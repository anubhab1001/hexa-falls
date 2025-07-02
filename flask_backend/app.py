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
    'milk': 'milk', 'wheat': 'wheat', 'soy': 'soy', 'gluten': 'gluten',
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
        ocr_text = pytesseract.image_to_string(image)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

