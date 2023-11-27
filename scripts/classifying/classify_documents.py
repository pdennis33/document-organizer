from .classify_exact_match import classify_documents, load_rules
import shutil
from datetime import datetime
import os


def copy_and_rename_files(classified_docs, source_img_directory, target_base_directory):
    vendor_file_count = {}

    for text_file, (category, vendor_name) in classified_docs.items():
        if category != "unknown" and vendor_name is not None:
            date_stamp = datetime.now().strftime('%Y%m%d')
            vendor_key = f"{vendor_name}_{date_stamp}"

            # Initialize or increment the file counter for this vendor
            if vendor_key not in vendor_file_count:
                vendor_file_count[vendor_key] = 1
            else:
                vendor_file_count[vendor_key] += 1

            sequence = f"_{vendor_file_count[vendor_key]:02d}"
            new_filename = f"{vendor_name}{sequence}_{date_stamp}.jpg"

            source_path = os.path.join(source_img_directory, text_file.replace('.txt', '.jpg'))
            target_path = os.path.join(target_base_directory, category, vendor_name, new_filename)

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy(source_path, target_path)  # Copy the file
            print(f"Copied and renamed file {text_file} to {target_path}")
        else:
            print(f"Skipped unknown category file: {text_file}")


def classify_and_rename(cleaned_text_dir, raw_images_dir, final_output_dir, rules_path):
    # Classify documents
    rules = load_rules(rules_path)
    classified_documents = classify_documents(cleaned_text_dir, rules)

    # Run the copy and rename operation
    copy_and_rename_files(classified_documents, raw_images_dir, final_output_dir)


if __name__ == "__main__":
    # Paths for classification
    text_directory = '../../data/text/cleaned/'
    rules_path = '../../config/rules.json'

    # Classify documents
    rules = load_rules(rules_path)
    classified_documents = classify_documents(text_directory, rules)

    # Paths to your directories
    source_img_directory = '../../data/images/inbox/'
    target_base_directory = '../../data/images/classified/'

    # Run the copy and rename operation
    copy_and_rename_files(classified_documents, source_img_directory, target_base_directory)
