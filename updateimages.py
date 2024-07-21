import json

# Paths to the JSON files
existing_data_file = 'translated_quiz_data.json'  # File with the existing image paths
new_image_data_file = 'data.json'  # File with the new image paths
output_file = 'Webserver/data/translated_quiz_data.json'  # Output file for the updated data

# Load the new image paths data
with open(new_image_data_file, 'r', encoding='utf-8') as file:
    new_image_data = json.load(file)

# Create a mapping from question_number to image_file
image_path_mapping = {
    item['question_number']: item['image_file']
    for item in new_image_data
}

# Load the existing JSON data
with open(existing_data_file, 'r', encoding='utf-8') as file:
    existing_data = json.load(file)

# Update the has_image field with the new paths
for item in existing_data:
    question_id = item.get('id')
    if question_id in image_path_mapping:
        item['has_image'] = image_path_mapping[question_id]

# Save the updated data to a new file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, indent=4, ensure_ascii=False)

print("Image paths updated successfully.")
