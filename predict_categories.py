import pandas as pd
import unicodedata as ud
from sklearn.cluster import KMeans
import joblib

custom_stop_words = [""]

# Load custom trained category classifier along with the vectorizer
classifier = joblib.load('category_classifier_model.pkl')
loaded_vectorizer = joblib.load('vectorizer_classifier.pkl')
labels = joblib.load('labels.pkl')
# ------

# Load collected data form previous step
df = pd.read_excel('total_2.xlsx', engine='openpyxl')
df = df.drop_duplicates()
df = df.dropna(subset=['ppu']) # make sure every entry has a price
# ------

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


# Store the preprocessed text in the df
df['preprocessed_text'] = df['name'].apply(preprocess_text)
v_matrix = loaded_vectorizer.transform(df['preprocessed_text'])

predicted_class = classifier.predict(v_matrix)

class_mapping = {   0:'SNACKS - ΚΑΒΑ',
                    1:'ΕΤΟΙΜΑ',
                    2:'ΚΑΤΑΨΥΞΗ',
                    3:'ΚΑΤΟΙΚΙΔΙΑ',
                    4:'ΚΡΕΑΤΙΚΑ',
                    5:'ΛΑΧΑΝΙΚΑ',
                    6:'ΠΡΟΣΩΠΙΚΗ',
                    7:'ΠΡΩΙΝΟ',
                    8:'ΣΠΙΤΙ',
                    9:'ΤΥΠΟΠΟΙΗΜΕΝΑ',
                    10:'ΧΑΡΤΙΚΑ',
                    11:'ΨΑΡΙΑ',
                    12:'ΨΥΓΕΙΟ',
                    13:'ΨΩΜΙΑ'
                }

predicted_class_names = [class_mapping[label] for label in predicted_class]
df['pred'] = predicted_class_names # Holds the category that is showed in APP

# ------
# ------
# ------

# Choose a subset of the data to cluster
df1 = pd.DataFrame(columns=df.columns)
df1 = df1.append(df[(df['pred'] != 'ΛΑΧΑΝΙΚΑ') & (df['pred'] != 'ΨΩΜΙΑ') & (df['pred'] != 'ΚΑΤΟΙΚΙΔΙΑ') & (df['pred'] != 'ΚΑΤΑΨΥΞΗ')])
df1['merged'] = df['preprocessed_text'] + ' ' + df['pred'].apply(preprocess_text)

v_matrix_df1 = loaded_vectorizer.transform(df1['merged'])

# ------
# ------
# ------

# Used Elbow method to identify the optimal number of clusters
# Clustered the products into 27 clusters
kmeans = KMeans(n_clusters=27, random_state=42)
kmeans.fit(v_matrix_df1)

# Get the predicted clusters from the model
predicted_clusters = kmeans.labels_
predicted_clusters = kmeans.predict(v_matrix_df1)

# Add the cluster labels back to the DataFrame
df1['cluster_label'] = predicted_clusters

# Continue the data analysis based on the clustered label




