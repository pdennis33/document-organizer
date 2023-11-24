import os
from sklearn.feature_extraction.text import TfidfVectorizer


def load_cleaned_text(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                documents.append(file.read())
    return documents


def extract_features(documents_directory):
    cleaned_text_directory = documents_directory
    cleaned_documents = load_cleaned_text(cleaned_text_directory)

    # Create the TF-IDF feature matrix
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(cleaned_documents)
    return feature_matrix, vectorizer
