'''

import fitz


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

if __name__ == "__main__":
    pdf_path = 'DomandeB.pdf'  # Replace with your PDF file path
    num_unique_images = extract_images_from_pdf(pdf_path)
    print(f"Found {num_unique_images} unique images.")
    '''
import time
import requests
import fitz
import re
import json


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
                    'has_image': f"images\DomandeB.pdf-image-{str(image_count).zfill(3)}.jpg"
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


pdf_path = 'DomandeB.pdf'

quiz_data = extract_quiz_data(pdf_path)


def translate(question):
    full_response = "Error"
    url = 'http://localhost:11434/api/generate'

    task = "Translate this Text from Italian to german."
    information = "Only output the translated text not anything else," \
                  "some information on translations: " \
                  "segnale=Verkehrszeichen"

    data = {
        "model": "gemma2",
        "prompt": f"{task} {information} : {question}"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # Assuming the response text contains multiple JSON objects
        responses = response.text.strip().split('\n')

        # Concatenate all response fields
        full_response = ''.join(json.loads(line)['response'] for line in responses if line.strip())


    else:
        print("Failed to get a response. Status code:", response.status_code)

    return full_response


try:
    with open("questions.json", "r") as file:
        existing_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    existing_data = []


for quiz in quiz_data:
    old_time = time.time()

    translated_text = translate(quiz["text"])

    new_time = time.time()
    print(f"Took {(new_time - old_time)}s to translate question {quiz['id']}")
    # Create new entry
    new_entry = {
        'id': quiz['id'],
        'text': quiz['text'],
        'text_translated': translated_text,
        'is_true': quiz['is_true'],
        'has_image': quiz['has_image']
    }

    existing_data.append(new_entry)

    with open("questions.json", "w") as file:
        json.dump(existing_data, file)
