import json
import os
import re
from fuzzywuzzy import process


def load_rules(path_to_json):
    with open(path_to_json, 'r') as file:
        return json.load(file)


def classify_document_from_vendor_name(text, rules):
    # Extract all vendor names for fuzzy matching
    vendor_scores = {}
    all_vendors = list(rules['vendors'].keys())

    # Perform token_set_ratio on all vendors and store the scores
    for vendor in all_vendors:
        vendor_scores[vendor] = process.fuzz.token_set_ratio(text, vendor)

    # Find the highest score
    max_score = max(vendor_scores.values())

    # Filter vendors with the highest score
    top_vendors = [vendor for vendor, score in vendor_scores.items() if score == max_score]

    # If there are multiple vendors with the same highest score, use regex to break the tie
    if len(top_vendors) > 1:
        vendor_regex = re.compile('|'.join(map(re.escape, top_vendors)), re.IGNORECASE)
        regex_match = vendor_regex.search(text)
        if regex_match:
            best_match = regex_match.group(0)
            matched_category = rules['vendors'][best_match]
            return matched_category, best_match.replace(" ", "_")

    # If there's only one top vendor, no need for regex
    elif len(top_vendors) == 1:
        best_match = top_vendors[0]
        matched_category = rules['vendors'][best_match]
        return matched_category, best_match.replace(" ", "_")

    return "unknown", None



# def classify_document_from_vendor_name(text, rules):
#     for category, definition in rules['categories'].items():
#         # Using fuzzy matching to find the closest vendor name
#         # It's important to note the usage of the token_set_ratio scorer. This scorer is much more
#         # effective when searching for a substring within a string. For example, we are searching
#         # for a vendor name within a document text. TLDR: it groups words together into tokens in both
#         # the search string and the target string, and then compares the tokens to each other.
#         match, score = process.extractOne(text, definition['vendors'], scorer=process.fuzz.token_set_ratio)
#         if score > 80:
#             return category, match.replace(" ", "_")
#     return "unknown", None


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
                category, vendor_name = classify_document_from_vendor_name(text, rules)

                if category == "unknown":
                    if previous_classification is not None and is_search_term_match(text,
                                                                                    rules['categories'][
                                                                                        previous_classification[0]][
                                                                                        'search_terms']):
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
