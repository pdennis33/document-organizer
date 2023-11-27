import re
import os


def clean_text(text, remove_digits):
    # Convert to lowercase
    text = text.lower()
    # Replace - with a space
    text = text.replace('-', ' ')
    # Remove new lines
    # text = text.replace('\n', ' ')
    # Remove special characters and (conditionally) digits
    if remove_digits:
        text = re.sub(r'[^a-zA-Z\s]', '', text, re.I | re.A)
    else:
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text, re.I | re.A)
    # Remove multiple spaces
    text = re.sub(r'[ \t\n\r\f\v]+', ' ', text)
    # Strip leading and trailing whitespace
    text = text.strip()
    return text


def clean_documents(raw_text_dir, cleaned_text_dir, remove_digits=False):
    for filename in os.listdir(raw_text_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(raw_text_dir, filename), 'r') as raw_file:
                file_text = raw_file.read()
                cleaned_text = clean_text(file_text, remove_digits)
                # Save the cleaned text to a file
                with open(os.path.join(cleaned_text_dir, filename), 'w') as file:
                    file.write(cleaned_text)
