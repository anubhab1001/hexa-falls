<<<<<<< HEAD
import React, { useState, useCallback } from 'react';
import { XCircle, Loader2, CheckCircle } from 'lucide-react';
=======
// src/pages/UploadPage.jsx

import React, { useState, useCallback } from "react";
import { XCircle, Loader2, CheckCircle } from "lucide-react";
const backend_url = import.meta.env.VITE_BACKEND_URL;
>>>>>>> friend

const ALLERGEN_MAPPING = {
  milk: "milk",
  wheat: "wheat",
  soy: "soy",
  gluten: "gluten",
  egg: "egg",
  eggs: "egg",
  peanut: "peanut",
  nuts: "tree nuts",
  fish: "fish",
  shellfish: "shellfish",
  sesame: "sesame",
  lait: "milk",
  blé: "wheat",
  soja: "soy",
  beurre: "butter",
  œufs: "egg",
  arachide: "peanut",
  noisettes: "hazelnuts",
  leche: "milk",
  trigo: "wheat",
  huevo: "egg",
  cacahuete: "peanut",
  casein: "milk",
  lactose: "milk",
  albumin: "egg",
};

const preprocessText = (text) => {
<<<<<<< HEAD
  let cleaned = text.toLowerCase().replace(/[^À-ÿ\w\s]/gi, ' ');
  ['contains', 'may contain', 'ingredients', 'ingredientes', 'ingrédients','INGREDIENTS']
    .forEach(term => cleaned = cleaned.replace(term, ''));
=======
  let cleaned = text.toLowerCase().replace(/[^À-ÿ\w\s]/gi, " ");
  [
    "contains",
    "may contain",
    "ingredients",
    "ingredientes",
    "ingrédients",
  ].forEach((term) => (cleaned = cleaned.replace(term, "")));
>>>>>>> friend
  return cleaned;
};

const detectAllergensOffline = (text) => {
  const cleaned = preprocessText(text);
  const words = cleaned.split(/\s+/);
  const found = new Set();
  for (const word of words) {
    if (ALLERGEN_MAPPING[word]) found.add(ALLERGEN_MAPPING[word]);
  }
  return Array.from(found);
};

const UploadPage = () => {
  const [textInput, setTextInput] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [apiEndpoint] = useState(backend_url);

  const resetAnalysis = () => {
    setTextInput("");
    setImageFile(null);
    setAnalysisResult(null);
    setError(null);
  };

  const analyzeText = useCallback(async () => {
    setIsAnalyzing(true);
    setError(null);

    try {
      if (imageFile) {
        const formData = new FormData();
        formData.append("image", imageFile);

        const response = await fetch(`${apiEndpoint}/ocr-translate-predict`, {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "API error");

        setAnalysisResult({
          safe: Object.keys(data.prediction)[0] === "No allergens detected",
          allergens: Object.keys(data.prediction),
          confidence: data.confidence || 95,
<<<<<<< HEAD
          rawText: `OCR: ${data.ocr_text || 'N/A'}\n\nTranslated: ${data.translated_text || 'N/A'}`
=======
          rawText: data.translated_text || data.ocr_text,
>>>>>>> friend
        });
      } else if (textInput.trim()) {
        const response = await fetch(`${apiEndpoint}/predict`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ingredients: textInput }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "API error");

        setAnalysisResult({
          safe: Object.keys(data.prediction)[0] === "No allergens detected",
          allergens: Object.keys(data.prediction),
          confidence: data.confidence || 95,
          rawText: textInput,
        });
      } else {
        throw new Error("Please provide ingredients via text or image.");
      }
    } catch (err) {
      console.warn("Fallback to offline:", err.message);
      const fallbackText = imageFile ? '[Fallback: offline mode unavailable for image]' : textInput;
      const offlineDetected = detectAllergensOffline(fallbackText);
      setAnalysisResult({
        safe: offlineDetected.length === 0,
        allergens:
          offlineDetected.length > 0
            ? offlineDetected
            : ["No allergens detected"],
        confidence: 80,
<<<<<<< HEAD
        rawText: fallbackText
=======
        rawText: textInput,
>>>>>>> friend
      });
      setError("⚠️ Using fallback detection. Server unreachable or returned an error.");
    } finally {
      setIsAnalyzing(false);
    }
  }, [textInput, imageFile, apiEndpoint]);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center">
<<<<<<< HEAD
          <h1 className="text-3xl font-bold text-gray-900">SafeBite Allergen Detection</h1>
          <p className="text-gray-600 mt-2">Upload image or enter ingredients manually</p>
=======
          <h1 className="text-3xl font-bold text-gray-900">
            SafeBite Allergen Detection
          </h1>
          <p className="text-gray-600 mt-2">
            Enter or upload food label to detect allergens
          </p>
>>>>>>> friend
        </div>

        {error && (
          <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
            <div className="flex items-center">
              <XCircle className="h-5 w-5 text-yellow-500 mr-2" />
              <p className="text-yellow-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="bg-white shadow rounded-lg p-6">
          <label className="block mb-2 font-medium text-gray-700">
            Upload Image
          </label>
          <div
            className={`flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-6 mb-4 transition ${
              imageFile
                ? "border-emerald-500 bg-emerald-50"
                : "border-gray-300 bg-gray-100 hover:border-emerald-400"
            }`}
          >
            {imageFile ? (
              <div className="flex flex-col items-center">
                <img
                  src={URL.createObjectURL(imageFile)}
                  alt="Preview"
                  className="w-32 h-32 object-cover rounded mb-2 border border-emerald-300"
                />
                <button
                  type="button"
                  onClick={() => setImageFile(null)}
                  className="text-red-500 text-xs underline mb-2"
                >
                  Remove Image
                </button>
              </div>
            ) : (
              <>
                <svg
                  className="w-10 h-10 text-emerald-400 mb-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16V4a1 1 0 011-1h8a1 1 0 011 1v12m-4 4v-4m0 0l-2 2m2-2l2 2"
                  />
                </svg>
                <span className="text-gray-500 mb-2 text-sm">
                  Drag & drop or click to select an image
                </span>
                <label className="cursor-pointer bg-emerald-600 text-white px-4 py-2 rounded hover:bg-emerald-700 transition text-sm">
                  Choose File
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setImageFile(e.target.files[0])}
                    className="hidden"
                  />
                </label>
              </>
            )}
          </div>
          <textarea
            rows={5}
            placeholder="Or type ingredients (e.g. milk, wheat, egg...)"
            value={textInput}
            onChange={(e) => {
              setTextInput(e.target.value);
              setError(null);
            }}
            disabled={isAnalyzing}
            className="w-full border border-gray-300 rounded-md p-3 focus:ring-2 focus:ring-emerald-500"
          />

          <button
            onClick={analyzeText}
            disabled={isAnalyzing || (!textInput.trim() && !imageFile)}
            className={`mt-4 w-full py-2 px-4 rounded-md text-white font-medium ${
              isAnalyzing || (!textInput.trim() && !imageFile)
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-emerald-600 hover:bg-emerald-700"
            }`}
          >
            {isAnalyzing ? (
              <span className="flex items-center justify-center">
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                Analyzing...
              </span>
            ) : (
              "Analyze"
            )}
          </button>
        </div>

        {analysisResult && (
          <div className="bg-white shadow rounded-lg p-6 space-y-4">
            <div className="text-center">
              <div
                className={`mx-auto flex items-center justify-center h-16 w-16 rounded-full ${
                  analysisResult.safe ? "bg-green-100" : "bg-red-100"
                }`}
              >
                {analysisResult.safe ? (
                  <CheckCircle className="h-10 w-10 text-green-600" />
                ) : (
                  <XCircle className="h-10 w-10 text-red-600" />
                )}
              </div>
              <h3
                className={`mt-3 text-2xl font-bold ${
                  analysisResult.safe ? "text-green-600" : "text-red-600"
                }`}
              >
                {analysisResult.safe
                  ? "No Allergens Detected"
                  : "Allergens Found"}
              </h3>
              <p className="text-gray-500">
                Confidence: {analysisResult.confidence}%
              </p>
            </div>

            {!analysisResult.safe && (
              <div className="bg-red-50 p-4 rounded-lg">
<<<<<<< HEAD
                <h4 className="font-semibold text-red-800 mb-2">Detected Allergens: </h4>
=======
                <h4 className="font-semibold text-red-800 mb-2">
                  Detected Allergens:
                </h4>
>>>>>>> friend
                <div className="flex flex-wrap gap-2">
                  {analysisResult.allergens.map((allergen, idx) => (
                    <span
                      key={idx}
                      className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                    >
                      {allergen}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="border-t pt-4">
              <h4 className="font-medium text-gray-800 mb-1">Analyzed Text:</h4>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">
                {analysisResult.rawText}
              </p>
            </div>

            <button
              onClick={resetAnalysis}
              className="w-full py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-gray-700"
            >
              Start New Analysis
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
