import pandas as pd
import re

# Read the labeled data
df = pd.read_csv('../../data_prep/file_labels.csv')


# Function to clean text
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I | re.A)
    return text


# Loop through the DataFrame and clean text
for index, row in df.iterrows():
    file_path = f"../../data/text/raw/{row['text_file_name']}"
    with open(file_path, 'r') as file:
        fileText = file.read()
        cleaned_text = clean_text(fileText)
        # Save the cleaned text to a file
        with open(file_path.replace('raw', 'cleaned'), 'w') as file:
            file.write(cleaned_text)
        # You can now use 'cleaned_text' for further processing
