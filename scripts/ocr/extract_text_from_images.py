import os
import pytesseract


def extract_text_from_images_and_save(image_directory, text_directory):
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            try:
                # Construct full file paths
                image_file = os.path.join(image_directory, filename)
                text_file = os.path.join(text_directory, f"{filename[:-4]}.txt")
                if os.path.isfile(text_file):
                    print(f"File {text_file} already exists, skipping...")
                    continue

                # Apply OCR to the image
                try:
                    text = pytesseract.image_to_string(image_file)
                except Exception as e:
                    print(f"OCR error on file {filename}: {e}")
                    continue

                # Save the extracted text to a file
                try:
                    with open(text_file, 'w') as file:
                        file.write(text)
                except Exception as e:
                    print(f"Error saving text for file {filename}: {e}")
                    continue

                print(f"Extracted text from {filename} and saved to {text_file}")
                print(f"_____________________________________________________________")

            except Exception as e:
                print(f"General error processing {filename}: {e}")


if __name__ == "__main__":
    # Specify the directory
    image_dir = '../../data/images/inbox'
    text_dir = "../../data/text/raw"
    extract_text_from_images_and_save(image_dir, text_dir)
