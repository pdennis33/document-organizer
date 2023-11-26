import json
import os
import re
from fuzzywuzzy import process


def load_rules(path_to_json):
    with open(path_to_json, 'r') as file:
        return json.load(file)


def customized_fuzzy_matching(query, document_text):
    # Break the document text into chunks
    words = document_text.split()
    query_length = len(query.split())
    chunks = [' '.join(words[i:i + query_length]) for i in range(len(words) - query_length + 1)]

    # Perform fuzzy matching with each chunk
    best_score = 0
    for chunk in chunks:
        score = process.fuzz.ratio(query, chunk)
        # If we get the maximum score, exit early
        if score == 100:
            return score
        best_score = max(best_score, score)

    return best_score


def classify_document(text, rules):
    # Attempt regex matching first
    for vendor, category in rules['vendors'].items():
        if re.search(rf"\b{re.escape(vendor)}\b", text, re.IGNORECASE):
            return category, vendor.replace(" ", "_")

    # Dictionary to hold scores for each vendor
    vendor_scores = {}

    # Use customized fuzzy matching and store scores
    for vendor in rules['vendors'].keys():
        vendor_scores[vendor] = customized_fuzzy_matching(vendor, text)

    # Find the highest score
    max_score = max(vendor_scores.values())

    # Find all vendors that have the highest score
    top_vendors = [vendor for vendor, score in vendor_scores.items() if score == max_score]

    # Handle ties or clear winner
    if len(top_vendors) > 1:
        return "tie", top_vendors
    elif len(top_vendors) == 1 and max_score > 80:  # Threshold
        matched_category = rules['vendors'][top_vendors[0]]
        return matched_category, top_vendors[0].replace(" ", "_")

    return "unknown", None


def is_search_term_match(text, search_terms):
    for keyword in search_terms:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            return True
    return False


def classify_documents(text_directory, rules):
    classified_docs = {}
    previous_classification = None

    # Sort files alphabetically
    sorted_files = sorted(os.listdir(text_directory))

    for filename in sorted_files:
        if filename.endswith('.txt'):
            file_path = os.path.join(text_directory, filename)
            with open(file_path, 'r') as file:
                text = file.read()

                # Start with trying an exact match based on vendor name
                # If an exact match is not found, try fuzzy matching
                category, vendor_name = classify_document(text, rules)

                if category == "tie":
                    print(f"Could not classify document due to a tie between vendors: {vendor_name}")
                elif category == "unknown":
                    if previous_classification is not None and is_search_term_match(text, rules['categories'][
                        previous_classification[0]]['search_terms']):
                        category, vendor_name = previous_classification
                else:
                    previous_classification = (category, vendor_name)

                classified_docs[filename] = (category, vendor_name)
                if category != "unknown":
                    print(f"File: {filename} | Category: {category} | Vendor: {vendor_name}")
                    # print(f"{category}")
                    # print(f"{vendor_name}")
                else:
                    print(f"UNKNOWN CATEGORY: File: {filename} | Category: {category}")
    return classified_docs


# Optionally, you can still have a standalone execution capability
if __name__ == "__main__":
    text_directory = '../../data/text/cleaned/'
    rules_path = '../../config/rules.json'

    rules = load_rules(rules_path)
    classified_documents = classify_documents(text_directory, rules)
