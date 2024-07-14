import fitz
import re
from deep_translator import GoogleTranslator
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
                    'numero_domanda': numero_domanda,
                    'testo_domanda': testo_domanda,
                    'risposta_corretta': risposta_corretta,
                    'has_image': f"images\DomandeB.pdf-image-{str(image_count).zfill(3)}.jpg"
                    # Indicates if there is an image on the page
                })
                image_count += 1

            else:
                quiz_data.append({
                    'numero_domanda': numero_domanda,
                    'testo_domanda': testo_domanda,
                    'risposta_corretta': risposta_corretta,
                    'has_image': None  # Indicates if there is an image on the page
                })

    print(f"found {image_count} images")
    return quiz_data


pdf_path = 'DomandeB.pdf'
quiz_data = extract_quiz_data(pdf_path)
print(f"Extracted {len(quiz_data)} questions from the PDF")


def translate_questions_create_new_array(quiz_data):
    i = 1
    translated_quiz_data = []
    for item in quiz_data:
        translated_item = {
            'numero_domanda': item['numero_domanda'],
            'testo_domanda': GoogleTranslator(source='it', target='de').translate(item['testo_domanda']),
            'risposta_corretta': item['risposta_corretta'],
            'has_image': item['has_image']
        }
        translated_quiz_data.append(translated_item)
        print(f"Translated question {i}")
        i +=1
    return translated_quiz_data


# Assuming quiz_data is already populated with your data
translated_quiz_data = translate_questions_create_new_array(quiz_data)

# Save the translated quiz data to a JSON file
with open('quiz_data.json', 'w') as outfile:
    json.dump(translated_quiz_data, outfile, ensure_ascii=False, indent=4)
