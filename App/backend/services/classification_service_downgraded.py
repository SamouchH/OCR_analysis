import joblib
import os
import re

class ClassificationService:
    def __init__(self):
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models/Classification_model')
        self.vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer.joblib'))
        self.classifier = joblib.load(os.path.join(model_dir, 'classifier.joblib'))
        self.mlb = joblib.load(os.path.join(model_dir, 'multilabel_binarizer.joblib'))

    def preprocess_text(self, text):
        # Supprimez les caractères non alphanumériques et convertissez en minuscules
        return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

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