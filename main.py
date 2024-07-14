import fitz
import re

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
                    'has_image': f"images\DomandeB.pdf-image-{str(image_count).zfill(3)}.jpg"  # Indicates if there is an image on the page
                })
                image_count += 1

            else:
                quiz_data.append({
                    'numero_domanda': numero_domanda,
                    'testo_domanda': testo_domanda,
                    'risposta_corretta': risposta_corretta,
                    'has_image': None # Indicates if there is an image on the page
                })

    print(f"found {image_count} images")
    return quiz_data

pdf_path = 'DomandeB.pdf'
quiz_data = extract_quiz_data(pdf_path)
print(f"Extracted {len(quiz_data)} questions from the PDF")


