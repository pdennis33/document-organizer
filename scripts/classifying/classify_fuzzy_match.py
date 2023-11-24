import json
import os
from fuzzywuzzy import process


def load_rules(path_to_json):
    with open(path_to_json, 'r') as file:
        return json.load(file)


def classify_document(text, rules, threshold):
    category_scores = {}

    # Iterate over categories to calculate average score per category
    for category, keywords in rules['categories'].items():
        total_score = 0
        for keyword in keywords:
            # Use extractOne to get the best match and its score
            match, score = process.extractOne(keyword, text.split())
            print(f"Keyword: {keyword} | Match: {match} | Score: {score}")
            total_score += score
        average_score = total_score / len(keywords)
        category_scores[category] = average_score

    # Find the best category if its score is above the threshold
    best_category = max(category_scores, key=category_scores.get)
    if category_scores[best_category] >= threshold:
        return best_category, category_scores[best_category]
    else:
        return "unknown", category_scores[best_category]


def process_text_files(text_directory, rules, threshold=95.0):
    classified_docs = {}
    for filename in os.listdir(text_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_directory, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                category, score = classify_document(text, rules, threshold)
                classified_docs[filename] = (category, score)
                print(f"File: {filename} | Category: {category} | Score: {score}")
    return classified_docs


# Define the path to your cleaned text files and rules
text_directory = '../../data/text/cleaned/'
rules_path = '../../config/rules.json'

# Load your classification rules
rules = load_rules(rules_path)

# Classify all documents in the directory
classified_documents = process_text_files(text_directory, rules, 90.5)

# Output the classification results
for filename, category in classified_documents.items():
    if category[0] == 'unknown':
        print(f"Document {filename} is classified as {category}")
