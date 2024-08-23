import joblib
import os
import re
import json

class ClassificationService:
    def __init__(self):
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models/Classification_model')
        self.vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer.joblib'))
        self.classifier = joblib.load(os.path.join(model_dir, 'classifier.joblib'))
        self.mlb = joblib.load(os.path.join(model_dir, 'multilabel_binarizer.joblib'))

    def preprocess_text(self, text):
        # Essayez de parser le JSON si le texte ressemble à du JSON
        try:
            data = json.loads(text)
            if isinstance(data, list):
                # Extraire toutes les transcriptions
                text = ' '.join([item['transcription'] for item in data if 'transcription' in item])
        except json.JSONDecodeError:
            # Si ce n'est pas du JSON, utilisez le texte tel quel
            pass

        # Nettoyage de base
        text = re.sub(r'[^\w\s]', '', text)
        return text.lower()

    def classify(self, text):
        preprocessed_text = self.preprocess_text(text)
        text_vectorized = self.vectorizer.transform([preprocessed_text])
        prediction = self.classifier.predict(text_vectorized)
        predicted_labels = self.mlb.inverse_transform(prediction)[0]

        result = {
            'manufacturer': '',
            'model': '',
            'serial_number': '',
            'date': ''
        }

        for label in predicted_labels:
            for key in result.keys():
                if key in label:
                    result[key] = label.replace(f"{key}_", "")
                    break

        return result

classification_service = ClassificationService()