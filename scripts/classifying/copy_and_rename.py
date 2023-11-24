import json
import os
import shutil
from datetime import datetime
from fuzzywuzzy import process


def load_rules(path_to_json):
    with open(path_to_json, 'r') as file:
        return json.load(file)


def find_vendor(text, vendors):
    # Using fuzzy matching to find the closest vendor name
    match, score = process.extractOne(text, vendors)
    if score > 80:  # You can adjust the score threshold
        return match.replace(" ", "_")  # Replace spaces with underscores
    return None


def move_and_rename_files(classified_docs, source_directory, target_base_directory, vendors):
    for filename, category in classified_docs.items():
        file_path = os.path.join(source_directory, filename)
        with open(file_path, 'r') as file:
            text = file.read()

        vendor_name = find_vendor(text, vendors)
        if vendor_name:
            new_filename = f"{vendor_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        else:
            new_filename = f"document_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        # Define source and target paths for the image file
        image_file = filename.replace('.txt', '.jpg')  # Assuming image has same name as text file
        source_image_path = os.path.join('path/to/original/images', image_file)
        target_image_path = os.path.join(target_base_directory, category, new_filename)

        # Create target directory if it doesn't exist
        os.makedirs(os.path.dirname(target_image_path), exist_ok=True)

        # Move and rename the image file
        shutil.move(source_image_path, target_image_path)
        print(f"Moved and renamed file {image_file} to {target_image_path}")


# Example usage
rules = load_rules('path/to/rules.json')
# classified_documents = {'doc1.txt': 'veterinary', 'doc2.txt': 'dental', ...}  # Use your actual classification results
source_directory = 'path/to/cleaned/text/directory'
target_base_directory = 'path/to/sorted/documents'

# move_and_rename_files(classified_documents, source_directory, target_base_directory, rules['vendors'])
