<<<<<<< HEAD
'''# ✅ Updated app.py for SafeBite (Offline-ready with text-only prediction)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import re

app = Flask(__name__)
CORS(app, resources={
    r"/predict": {"origins": "*", "methods": ["POST", "OPTIONS", "GET"]}
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
            # "/predict-image": "POST with image file" (currently disabled)
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

# 🔕 Image-based analysis disabled for offline compatibility
# @app.route('/predict-image', methods=['POST'])
# def predict_from_image():
#     return jsonify({"error": "Image analysis is currently disabled."}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)'''



=======
>>>>>>> friend
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import io
import pickle
import re
from googletrans import Translator
import os

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
try:
    with open('model/safebite_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('model/safebite_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print("Model loading error:", e)
    model = None
    vectorizer = None

ALLERGEN_MAPPING = {
    'milk': 'milk', 'wheat flour' : 'wheat','wheat': 'wheat', 'soy': 'soy', 'gluten': 'gluten',
    'egg': 'egg', 'eggs': 'egg', 'peanut': 'peanut', 'nuts': 'tree nuts',
    'fish': 'fish', 'shellfish': 'shellfish', 'sesame': 'sesame',
    'lait': 'milk', 'blé': 'wheat', 'soja': 'soy', 'beurre': 'butter',
    'œufs': 'egg', 'arachide': 'peanut', 'noisettes': 'hazelnuts',
    'leche': 'milk', 'trigo': 'wheat', 'huevo': 'egg', 'cacahuete': 'peanut',
    'casein': 'milk', 'lactose': 'milk', 'albumin': 'egg'
}
TARGET_ALLERGENS = sorted(set(ALLERGEN_MAPPING.values()))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    for term in ['contains', 'may contain', 'ingredients', 'ingredientes', 'ingrédients','INGREDIENTS']:
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
    return jsonify({"message": "SafeBite API is running."})

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

@app.route('/ocr-translate-predict', methods=['POST'])
def ocr_translate_predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image = Image.open(request.files['image'].stream)
        ocr_text = pytesseract.image_to_string(image,config="--psm 6")

        # Translate text to English
        translator = Translator()
        translated = translator.translate(ocr_text, dest='en').text

        detected = detect_allergens(translated)

        return jsonify({
            "ocr_text": ocr_text,
            "translated_text": translated,
            "prediction": {a: 1 for a in detected} if detected else {"No allergens detected": 0},
            "confidence": 95,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True) 
    

#1-7-25
'''from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import pickle
import re
from googletrans import Translator
import cv2
import numpy as np
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
with open('model/safebite_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model/safebite_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Allergen keyword map
ALLERGEN_MAPPING = {
    'milk': 'milk', 'wheat flour': 'wheat', 'wheat': 'wheat', 'soy': 'soy', 'gluten': 'gluten',
    'egg': 'egg', 'eggs': 'egg', 'peanut': 'peanut', 'nuts': 'tree nuts',
    'fish': 'fish', 'shellfish': 'shellfish', 'sesame': 'sesame',
    'lait': 'milk', 'blé': 'wheat', 'soja': 'soy', 'beurre': 'butter',
    'œufs': 'egg', 'arachide': 'peanut', 'noisettes': 'hazelnuts',
    'leche': 'milk', 'trigo': 'wheat', 'huevo': 'egg', 'cacahuete': 'peanut',
    'casein': 'milk', 'lactose': 'milk', 'albumin': 'egg'
}
TARGET_ALLERGENS = sorted(set(ALLERGEN_MAPPING.values()))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    for term in ['contains', 'may contain', 'ingredients', 'ingredientes', 'ingrédients', 'INGREDIENTS']:
        text = text.replace(term, '')
    return text.strip()

def fuzzy_match(word, mapping_keys, cutoff=0.8):
    match = get_close_matches(word, mapping_keys, n=1, cutoff=cutoff)
    return match[0] if match else None

def detect_allergens(text):
    cleaned_text = preprocess_text(text)
    words = cleaned_text.split()
    
    # ML Prediction
    vec = vectorizer.transform([cleaned_text])
    ml_preds = model.predict(vec)[0]
    ml_detected = {TARGET_ALLERGENS[i] for i, v in enumerate(ml_preds) if v == 1}
    
    # Keyword & fuzzy detection
    found_keywords = set()
    for word in words:
        match = fuzzy_match(word, ALLERGEN_MAPPING.keys())
        if match:
            found_keywords.add(ALLERGEN_MAPPING[match])
    
    return sorted(ml_detected.union(found_keywords))

def enhance_image_for_ocr(pil_image):
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(img)

@app.route('/')
def home():
    return jsonify({"message": "SafeBite API is running."})

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

@app.route('/ocr-translate-predict', methods=['POST'])
def ocr_translate_predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image = Image.open(request.files['image'].stream)
        enhanced_img = enhance_image_for_ocr(image)

        # OCR
        ocr_text = pytesseract.image_to_string(enhanced_img, config="--psm 6")

        # Translation
        translator = Translator()
        translated = translator.translate(ocr_text, dest='en').text

        detected = detect_allergens(translated)

        return jsonify({
            "ocr_text": ocr_text,
            "translated_text": translated,
            "prediction": {a: 1 for a in detected} if detected else {"No allergens detected": 0},
            "confidence": 95,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
=======
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
>>>>>>> friend


'''
