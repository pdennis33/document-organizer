import os
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_into_pages(pdf_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Initialize a global page counter
    global_page_counter = 1

    # Iterate through every file in the pdf_directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)

            # Open the PDF file
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)

                # Loop through each page and save it as a separate PDF
                for _ in range(len(reader.pages)):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[_])

                    # Format the output filename with leading zeros
                    output_filename = os.path.join(output_directory, f"{global_page_counter:03}.pdf")

                    # Save the individual page
                    with open(output_filename, 'wb') as output_file:
                        writer.write(output_file)

                    print(f"Saved page {global_page_counter} from '{filename}' as {output_filename}")
                    global_page_counter += 1


# Specify the path to the large PDF and the output directory
pdf_dir = '../../data/pdfs/inbox'
output_dir = '../../data/pdfs/processed'
split_pdf_into_pages(pdf_dir, output_dir)
