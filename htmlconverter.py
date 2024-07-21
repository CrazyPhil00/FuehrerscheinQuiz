from bs4 import BeautifulSoup
import base64
import json
import os
from PIL import Image
from io import BytesIO


# Function to decode and save the base64 image
def save_image(base64_str, file_name):
    # Extract the image data from base64
    image_data = base64_str.split(',')[1]
    image_data = base64.b64decode(image_data)

    # Convert the image data to an image
    image = Image.open(BytesIO(image_data))

    # Save the image
    image.save(file_name)


# Create a directory to store images
if not os.path.exists('newimages'):
    os.makedirs('newimages')

# Open and parse the HTML file
with open('DomandeB-converted.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Data structure to hold extracted data
data = []

# Find the table rows with the questions
rows = soup.find_all('tr')[1:]  # Skip the header row

for row in rows:
    cells = row.find_all('td')

    # Print out the number of cells for debugging
    print(f'Number of cells in row: {len(cells)}')

    # Check if there are enough cells
    if len(cells) < 4:
        print(f'Skipping row due to insufficient cells: {row}')
        continue

    question_number = cells[0].get_text(strip=True)
    question_text = cells[1].get_text(strip=True)
    answer = cells[2].get_text(strip=True)
    image_tag = cells[3].find('img')

    # Extract image data if present
    image_data = None
    image_file_name = None
    if image_tag:
        image_data = image_tag['src']
        image_file_name = f'newimages/{question_number}.jpg'
        save_image(image_data, image_file_name)

    # Append the data to the list
    data.append({
        'question_number': question_number,
        'question_text': question_text,
        'answer': answer,
        'image_file': image_file_name if image_data else None
    })

# Save the data to a JSON file
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Data extraction and image saving complete.")
