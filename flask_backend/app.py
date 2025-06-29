# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import re

app = Flask(__name__)
CORS(app, resources={
    r"/predict": {"origins": "*", "methods": ["POST", "OPTIONS", "GET"]},
    # r"/predict-image": {"origins": "*", "methods": ["POST", "OPTIONS"]}
})

# Load model & vectorizer
MODEL_PATH = 'model/safebite_model.pkl'
VECTORIZER_PATH = 'model/safebite_vectorizer.pkl'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, 'rb') as f:
    vectorizer = pickle.load(f)

ALLERGEN_MAPPING = {
    'milk': 'milk', 'wheat': 'wheat', 'soy': 'soy', 'gluten': 'gluten',
    'egg': 'egg', 'eggs': 'egg', 'peanut': 'peanut', 'nuts': 'tree nuts',
    'fish': 'fish', 'shellfish': 'shellfish', 'sesame': 'sesame',
    'lait': 'milk', 'blé': 'wheat', 'soja': 'soy', 'beurre': 'butter',
    'œufs': 'egg', 'arachide': 'peanut', 'noisettes': 'hazelnuts',
    'leche': 'milk', 'trigo': 'wheat', 'huevo': 'egg', 'cacahuete': 'peanut',
    'casein': 'milk', 'lactose': 'milk', 'albumin': 'egg'
}
TARGET_ALLERGENS = sorted(set(ALLERGEN_MAPPING.values())) + ['gluten']

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    for term in ['contains', 'may contain', 'ingredients', 'ingredientes', 'ingrédients']:
        text = text.replace(term, '')
    return text.strip()

def detect_allergens(text):
    cleaned_text = preprocess_text(text)
    vec = vectorizer.transform([cleaned_text])
    ml_preds = model.predict(vec)[0]
    found_keywords = {ALLERGEN_MAPPING[word] for word in cleaned_text.split() if word in ALLERGEN_MAPPING}
    detected = {TARGET_ALLERGENS[i] for i, v in enumerate(ml_preds) if v == 1}
    return sorted(detected.union(found_keywords))

@app.route('/')
def home():
    return jsonify({
        "message": "SafeBite Allergen Detection API",
        "endpoints": {
            "/predict": "POST with JSON {ingredients: text}"
            # "/predict-image": "POST with image file"
        }
    })

@app.route('/predict', methods=['POST'])
def predict_from_text():
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({"error": "Missing ingredients parameter"}), 400

        ingredients = data['ingredients']
        if not isinstance(ingredients, str):
            return jsonify({"error": "Ingredients must be a string"}), 400

        detected = detect_allergens(ingredients)

        return jsonify({
            "prediction": {a: 1 for a in detected} if detected else {"No allergens detected": 0},
            "confidence": 95,
            "status": "success",
            "input_text": ingredients[:500]
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

# Commented out image-based analysis
# @app.route('/predict-image', methods=['POST'])
# def predict_from_image():
#     return jsonify({"error": "Image analysis is currently disabled."}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
