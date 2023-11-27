import json
from ocr.extract_text_from_images import extract_text_from_images_and_save
from ocr.pre_process_text import clean_documents
from classifying.classify_documents import classify_and_rename


def main():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        raw_images_dir = config['raw_images_dir']
        final_output_dir = config['final_output_dir']
        raw_text_dir = config['raw_text_dir']
        cleaned_text_dir = config['cleaned_text_dir']
        rules_path = config['rules_path']

        # Step 1: Extract text from images
        extract_text_from_images_and_save(raw_images_dir, raw_text_dir)

        # Step 2: Preprocess the extracted text
        clean_documents(raw_text_dir, cleaned_text_dir)

        # Step 3: Classify and rename the images
        classify_and_rename(cleaned_text_dir, raw_images_dir, final_output_dir, rules_path)
    except Exception as e:
        print(f"General error processing: {e}")


if __name__ == "__main__":
    main()
