import fitz
import requests
import json
import re

def extract_images_from_pdf(pdf_path):
    """
    Extracts and counts unique images from a PDF document.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    int: Total number of unique images found in the PDF.
    """
    document = fitz.open(pdf_path)
    image_count = set()  # Use a set to track unique images

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        images_on_page = page.get_images(full=True)

        for img in images_on_page:
            # Generate a unique key for each image based on its index and width
            image_key = f"{img[0]}_{img[1]}"
            if image_key not in image_count:
                image_count.add(image_key)
                # Optionally, handle the image as needed (e.g., save it, log it, etc.)

    return len(image_count)

def extract_quiz_data(pdf_path):
    document = fitz.open(pdf_path)
    quiz_data = []

    image_count = 1

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        # Split the text into lines
        lines = text.split('\n')

        # Determine the number of lines to skip (adjust this value as needed)
        lines_to_skip = 2  # Example: skipping the first 2 lines

        # Remove the initial lines from consideration
        relevant_lines = lines[lines_to_skip:]

        # Rejoin the relevant lines back into a single string
        filtered_text = '\n'.join(relevant_lines)

        # Apply the regular expression to the filtered text
        pattern = re.compile(r'(\d+)\s*(.*?)(VERO|FALSO)\s*(?=\d+|$)', re.DOTALL | re.MULTILINE)
        matches = pattern.findall(filtered_text)

        # Check if there are any images on the page
        images_on_page = page.get_images(full=True)
        has_image = len(images_on_page) > 0

        for match in matches:
            numero_domanda, testo_domanda, risposta_corretta = match
            testo_domanda = ' '.join(testo_domanda.split()).strip('- ')

            if has_image:
                quiz_data.append({
                    'id': numero_domanda,
                    'text': testo_domanda,
                    'is_true': risposta_corretta,
                    'has_image': f"images\\DomandeB.pdf-image-{str(image_count).zfill(3)}.jpg"
                    # Indicates if there is an image on the page
                })
                image_count += 1

            else:
                quiz_data.append({
                    'id': numero_domanda,
                    'text': testo_domanda,
                    'is_true': risposta_corretta,
                    'has_image': None  # Indicates if there is an image on the page
                })

    print(f"found {image_count} images")
    return quiz_data

def translate_batch(questions):
    with open(".apikey", "r") as apifile:
        api_key = apifile.read()

    url = 'https://api.webraft.in/freeapi/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Prepare the data in JSON format
    data = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are a Translator. Translate each question from Italian to German. Only output the translation in a JSON format with \"id\" and \"text_translated\". USE \" IN JSON example: Translations Content: {\"translations\": [{\"id\": \"1814\", \"text_translated\": \"Das abgebildete Schild befindet sich in der Nähe eines Kontrollpunktes\"}]}\""
            },
            {
                "role": "user",
                "content": json.dumps({"questions": questions}, ensure_ascii=False)
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Debugging output: Print raw response text
    print("Raw API Response:", response.text)

    try:
        response_data = response.json()
        # Extract the content field directly
        translations_content = response_data.get('choices', [])[0].get('message', {}).get('content', '')

        # Print the content to check its structure
        print("Translations Content:", translations_content)

        # Parse the JSON content
        translations = json.loads(translations_content)
        return translations

    except (requests.exceptions.JSONDecodeError, KeyError, json.JSONDecodeError) as e:
        print("Error in translation response:", e)
        return None

def save_translated_data(filename, new_data):
    try:
        # Load existing data if the file already exists
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            # If file does not exist, initialize an empty list
            existing_data = []

        # Append new data to the existing data
        existing_data.extend(new_data)

        # Save the combined data back to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def main():
    pdf_path = 'DomandeB.pdf'
    quiz_data = extract_quiz_data(pdf_path)
    translated_quiz_data = []
    filename = 'translated_quiz_data.json'
    batch_size = 5

    for idx in range(0, len(quiz_data), batch_size):
        batch = quiz_data[idx:idx + batch_size]
        # Prepare the list of questions as JSON
        questions = [{"id": q['id'], "text": q['text']} for q in batch]

        # Get translations for the current batch
        translations_response = translate_batch(questions)

        if translations_response:
            # Create a dictionary for quick lookup
            translation_dict = {t['id']: t['text_translated'] for t in translations_response['translations']}

            # Update quiz data with translations
            for q in batch:
                translated_quiz_data.append({
                    'id': q['id'],
                    'text': q['text'],
                    'text_translated': translation_dict.get(q['id'], None),
                    'is_true': q['is_true'],
                    'has_image': q['has_image']
                })

        # Save the batch to file
        save_translated_data(filename, translated_quiz_data)
        translated_quiz_data = []

    # Handle any remaining questions not saved in the last batch
    if translated_quiz_data:
        save_translated_data(filename, translated_quiz_data)

if __name__ == "__main__":
    main()
