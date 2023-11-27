# main.py located in scripts/

from ocr.extract_text_from_images import extract_text_from_images_and_save
from ocr.pre_process_text import clean_documents
from classifying.classify_documents import classify_and_rename


def main():
    try:
        # Paths to your directories (adjust as necessary)
        # TEST directories
        raw_images_dir = '/Users/pauldennis/Development/document-organizer/data/images/inbox/'
        final_output_dir = '/Users/pauldennis/Development/document-organizer/data/images/classified/'

        # raw_images_dir = '/Users/PaulDennis/Dropbox/From_BrotherDevice'
        # final_output_dir = '/Users/PaulDennis/OneDrive/Documents/'
        raw_text_dir = '/Users/pauldennis/Development/document-organizer/data/text/raw/'
        cleaned_text_dir = '/Users/pauldennis/Development/document-organizer/data/text/cleaned/'
        rules_path = '/Users/pauldennis/Development/document-organizer/config/rules.json'

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
