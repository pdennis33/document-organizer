import pandas as pd
from feature_extraction import extract_features
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Read the labeled data
df = pd.read_csv('../../data_prep/file_labels.csv')

labels = []
document_names = []
# Loop through the DataFrame and clean text
for index, row in df.iterrows():
    document_names.append(row['text_file_name'])
    labels.append(row['label'])


cleaned_text_directory = '../../data/text/cleaned/'
# Extract features
feature_matrix, vectorizer = extract_features(cleaned_text_directory)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(feature_matrix, labels, test_size=0.2, random_state=42)

# Create and train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Test the model
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))
