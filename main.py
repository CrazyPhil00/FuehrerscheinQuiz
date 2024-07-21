import fitz
import re
import json


def extract_quiz_data(pdf_path):
    document = fitz.open(pdf_path)
    quiz_data = []
    image_count = 1
    used_images = set()

    # Open a log file for writing debug information
    with open('image_extraction_log.txt', 'w') as log_file:

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

            log_file.write(f"Page {page_num + 1} has {len(images_on_page)} images\n")

            for match in matches:
                numero_domanda, testo_domanda, risposta_corretta = match
                testo_domanda = ' '.join(testo_domanda.split()).strip('- ')

                # Initialize image path as None
                associated_image = None

                # Process images if available
                for img in images_on_page:
                    image_index = img[0]
                    if image_index not in used_images:
                        used_images.add(image_index)
                        image_path = f"images/DomandeB.pdf-image-{str(image_count).zfill(3)}.jpg"

                        # Save image to a file (if needed)
                        pix = fitz.Pixmap(document, image_index)
                        if pix.n - pix.alpha < 4:  # this is GRAY or RGB
                            pix.save(image_path)
                        else:  # CMYK: convert to RGB first
                            pix0 = fitz.Pixmap(fitz.csRGB, pix)
                            pix0.save(image_path)
                            pix0 = None
                        pix = None

                        associated_image = image_path
                        log_file.write(f"Associated image {image_path} with question {numero_domanda}\n")
                        image_count += 1
                        break  # Associate only the first unused image

                quiz_data.append({
                    'numero_domanda': numero_domanda,
                    'testo_domanda': testo_domanda,
                    'risposta_corretta': risposta_corretta,
                    'has_image': associated_image
                })

        log_file.write(f"Found {image_count - 1} unique images\n")

    return quiz_data


pdf_path = 'DomandeB.pdf'
quiz_data = extract_quiz_data(pdf_path)
#print(f"Extracted {quiz_data[len(quiz_data) - 1]} questions from the PDF")

# Save the translated quiz data to a JSON file

with open("images.json", "w") as file:
    json.dump(quiz_data, file)