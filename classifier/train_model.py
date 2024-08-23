import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Télécharger les ressources NLTK nécessaires
nltk.download('punkt')
nltk.download('stopwords')

# Chemins
TRAIN_CSV_PATH = 'dataframe_miro_train.csv'
TRAIN_TXT_PATH = '../data/processed/train_list.txt'
EVAL_CSV_PATH = 'dataframe_miro_eval.csv'  # Ajout du chemin pour le CSV d'évaluation
EVAL_TXT_PATH = '../data/processed/eval_list.txt'  # Ajout du chemin pour le TXT d'évaluation
MODEL_SAVE_PATH = './models/'

def load_data(csv_file, txt_file):
    # Charger les données du CSV
    df = pd.read_csv(csv_file, sep=';')
    
    # Charger les transcriptions du fichier TXT
    transcriptions = {}
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_path = os.path.basename(parts[0])
                transcription = parts[1]
                transcriptions[image_path] = transcription
    
    # Ajouter les transcriptions au DataFrame
    df['transcription'] = df['path'].apply(lambda x: transcriptions.get(x, ''))
    
    return df

def preprocess_text(text):
    # Conversion en minuscules
    text = text.lower()
    
    # Suppression des caractères spéciaux
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Suppression des stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Rejoindre les tokens
    return ' '.join(tokens)

def create_model():
    vectorizer = TfidfVectorizer(max_features=5000)
    classifier = OneVsRestClassifier(LinearSVC(random_state=42))
    return vectorizer, classifier

def train_model(X, y, vectorizer, classifier):
    X_vectorized = vectorizer.fit_transform(X)
    classifier.fit(X_vectorized, y)

def evaluate_model(X, y, vectorizer, classifier, set_name="Test"):
    X_vectorized = vectorizer.transform(X)
    y_pred = classifier.predict(X_vectorized)
    print(f"Classification Report for {set_name} Set:")
    print(classification_report(y, y_pred))

def main():
    # Charger et prétraiter les données d'entraînement
    train_df = load_data(TRAIN_CSV_PATH, TRAIN_TXT_PATH)
    train_df['processed_text'] = train_df['transcription'].apply(preprocess_text)
    
    # Charger et prétraiter les données d'évaluation
    eval_df = load_data(EVAL_CSV_PATH, EVAL_TXT_PATH)
    eval_df['processed_text'] = eval_df['transcription'].apply(preprocess_text)
    
    # Préparer les étiquettes
    mlb = MultiLabelBinarizer()
    y_train = mlb.fit_transform(train_df[['manufacturer', 'model', 'serial_number', 'date']].values)
    y_eval = mlb.transform(eval_df[['manufacturer', 'model', 'serial_number', 'date']].values)
    
    # Diviser les données d'entraînement
    X_train, X_test, y_train, y_test = train_test_split(train_df['processed_text'], y_train, test_size=0.2, random_state=42)
    
    # Créer et entraîner le modèle
    vectorizer, classifier = create_model()
    train_model(X_train, y_train, vectorizer, classifier)
    
    # Évaluer le modèle sur l'ensemble de test
    evaluate_model(X_test, y_test, vectorizer, classifier, "Test")
    
    # Évaluer le modèle sur l'ensemble d'évaluation séparé
    evaluate_model(eval_df['processed_text'], y_eval, vectorizer, classifier, "Evaluation")
    
    # Sauvegarder le modèle
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(MODEL_SAVE_PATH, 'vectorizer.joblib'))
    joblib.dump(classifier, os.path.join(MODEL_SAVE_PATH, 'classifier.joblib'))
    joblib.dump(mlb, os.path.join(MODEL_SAVE_PATH, 'multilabel_binarizer.joblib'))

if __name__ == "__main__":
    main()