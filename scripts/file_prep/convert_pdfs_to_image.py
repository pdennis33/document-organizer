import os
from pdf2image import convert_from_path


def convert_pdfs_to_images(pdf_directory, output_directory):
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            # Construct full file path
            pdf_file = os.path.join(pdf_directory, filename)

            # Convert PDF to image
            images = convert_from_path(pdf_file)

            # Save the first page as image (assuming single-page PDFs)
            for i, image in enumerate(images):
                image_file = os.path.join(output_directory, f"{filename[:-4]}_{i + 1}.jpg")
                image.save(image_file, 'JPEG')

            print(f"Converted {filename} to images")


# Specify the directories
pdf_dir = '../../data/pdfs/processed'
output_dir = '../../data/images/inbox'
convert_pdfs_to_images(pdf_dir, output_dir)
