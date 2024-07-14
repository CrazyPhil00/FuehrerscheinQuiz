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




import clipboard
import fitz
import re
from deep_translator import GoogleTranslator, ChatGptTranslator
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

i = 0

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")

chat = [
   {"role": "user", "content": "Hello, how are you?"},
   {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
   {"role": "user", "content": "I'd like to show off how chat templating works!"},
]

tokenizer.apply_chat_template(chat, tokenize=False)