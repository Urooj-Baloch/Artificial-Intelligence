import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from flask import Flask, jsonify, request
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, roc_auc_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class EmailSpamClassifier:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_trained = False

    def _preprocess_data(self, X):
        X = X.copy()
        if 'email_text' in X.columns:
            X['email_text'] = X['email_text'].str.lower()
        if 'sender_address' in X.columns:
            X['sender_address'] = X['sender_address'].str.lower()
            X['sender_domain'] = X['sender_address'].str.extract(r'@(.+)\.')[0]
        return X

    def _create_preprocessor(self):
        text_transformer = TfidfVectorizer(max_features=5000, stop_words='english')
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(
            transformers=[
                ('text', text_transformer, 'email_text'),
                ('num', numeric_transformer, ['email_length', 'num_hyperlinks']),
                ('cat', categorical_transformer, ['sender_domain'])
            ])
        return preprocessor

    def train(self, data_path, test_size=0.2, random_state=42):
        data = pd.read_csv(data_path)
        X = data.drop('is_spam', axis=1)
        y = data['is_spam']

        X_processed = self._preprocess_data(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=random_state, stratify=y)

        preprocessor = self._create_preprocessor()
        classifier = RandomForestClassifier(random_state=random_state, n_jobs=-1)

        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', classifier)
        ])

        param_grid = {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5]
        }

        print("Training model with GridSearchCV...")
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_
        self.preprocessor = preprocessor
        self.is_trained = True

        print("\nModel evaluation on test set:")
        self._evaluate(X_test, y_test)

        return grid_search.best_params_

    def _evaluate(self, X, y):
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        X_processed = self._preprocess_data(X)
        y_pred = self.model.predict(X_processed)
        y_proba = self.model.predict_proba(X_processed)[:, 1]

        print("Classification Report:")
        print(classification_report(y, y_pred))

        print(f"\nAccuracy: {accuracy_score(y, y_pred):.4f}")
        print(f"F1 Score: {f1_score(y, y_pred):.4f}")
        print(f"ROC AUC: {roc_auc_score(y, y_proba):.4f}")

        cm = confusion_matrix(y, y_pred)
        plt.figure(figsize=(6, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Not Spam', 'Spam'],
                    yticklabels=['Not Spam', 'Spam'])
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.show()

        return {
            'report': classification_report(y, y_pred, output_dict=True),
            'accuracy': accuracy_score(y, y_pred),
            'f1_score': f1_score(y, y_pred),
            'roc_auc': roc_auc_score(y, y_proba)
        }

    def predict(self, email_data):
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        if isinstance(email_data, dict):
            email_data = pd.DataFrame([email_data])
        elif isinstance(email_data, pd.DataFrame):
            pass
        else:
            raise ValueError("Input must be a dictionary or DataFrame")

        X_processed = self._preprocess_data(email_data)
        prediction = self.model.predict(X_processed)
        probability = self.model.predict_proba(X_processed)[:, 1]

        return {
            'prediction': int(prediction[0]),
            'probability': float(probability[0]),
            'is_spam': bool(prediction[0])
        }

    def save_model(self, filepath):
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"Model saved to {filepath}")

    @classmethod
    def load_model(cls, filepath):
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        if not model.is_trained:
            raise ValueError("Loaded model is not trained")
        print(f"Model loaded from {filepath}")
        return model

    def deploy_as_api(self, host='0.0.0.0', port=5000):
        if not self.is_trained:
            raise ValueError("Model must be trained before deployment")

        app = Flask(__name__)

        @app.route('/predict', methods=['POST'])
        def predict():
            try:
                data = request.json
                result = self.predict(data)
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 400

        @app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy', 'is_trained': self.is_trained})

        print(f"Starting API server at http://{host}:{port}")
        app.run(host=host, port=port)

if __name__ == '__main__':
    spam_classifier = EmailSpamClassifier()

    print("=== TRAINING ===")
    best_params = spam_classifier.train('emails_dataset.csv')
    print("Best parameters:", best_params)

    spam_classifier.save_model('spam_classifier_model.pkl')

    print("\n=== LOADING MODEL ===")
    loaded_classifier = EmailSpamClassifier.load_model('spam_classifier_model.pkl')

    print("\n=== SAMPLE PREDICTIONS ===")
    samples = [
        {
            'email_text': 'WIN A FREE IPHONE TODAY! Click here now!!!',
            'email_length': 150,
            'num_hyperlinks': 5,
            'sender_address': 'promo@spammy.com'
        },
        {
            'email_text': 'Hi John, just checking in about our meeting tomorrow',
            'email_length': 500,
            'num_hyperlinks': 0,
            'sender_address': 'john.smith@company.com'
        }
    ]

    for sample in samples:
        result = loaded_classifier.predict(sample)
        
        print(f"\nEmail: {sample['email_text'][:50]}...")
        print(f"Prediction: {'SPAM' if result['is_spam'] else 'Not Spam'}")
        print(f"Probability: {result['probability']:.4f}")
