import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import unicodedata as ud
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib

custom_stop_words = [""]

# Function to remove diacretics and accents
def strip_accents(s):
   return ''.join(c for c in ud.normalize('NFD', s)
                  if ud.category(c) != 'Mn')

# Preprocess text input
def preprocess_text(text):
    text = text.lower()
    text = strip_accents(text)
    tokens = []
    for i in text.split():
        tokens.append(i)
    tokens = [word for word in tokens if word not in custom_stop_words]
    return ' '.join(tokens)

# Load the train dataset
data = pd.read_excel('train_set.xlsx', engine='openpyxl')

# Preprocess the text data
datas = data['TEXT'].apply(preprocess_text)

# Split the data into features (X) and labels (y)
X = datas
y = data['LABEL']

# Encode the category labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# # Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

classifier = LogisticRegression(max_iter=1000)
classifier.fit(X_train_tfidf, y_train)

# # Make predictions on the test set
y_pred = classifier.predict(X_test_tfidf)

# # Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Save the model for future use
joblib.dump(classifier, 'category_classifier_model.pkl')

# Save the vectorizer too
joblib.dump(tfidf_vectorizer, 'vectorizer_classifier.pkl')

# Save the labels encoder for evaluation
joblib.dump(label_encoder, 'labels.pkl')