import React, { useState, useCallback } from 'react';
import { XCircle, Loader2, CheckCircle } from 'lucide-react';

const ALLERGEN_MAPPING = {
  milk: 'milk', wheat: 'wheat', soy: 'soy', gluten: 'gluten',
  egg: 'egg', eggs: 'egg', peanut: 'peanut', nuts: 'tree nuts',
  fish: 'fish', shellfish: 'shellfish', sesame: 'sesame',
  lait: 'milk', blé: 'wheat', soja: 'soy', beurre: 'butter',
  œufs: 'egg', arachide: 'peanut', noisettes: 'hazelnuts',
  leche: 'milk', trigo: 'wheat', huevo: 'egg', cacahuete: 'peanut',
  casein: 'milk', lactose: 'milk', albumin: 'egg'
};

const preprocessText = (text) => {
  let cleaned = text.toLowerCase().replace(/[^À-ÿ\w\s]/gi, ' ');
  ['contains', 'may contain', 'ingredients', 'ingredientes', 'ingrédients','INGREDIENTS']
    .forEach(term => cleaned = cleaned.replace(term, ''));
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
  const [apiEndpoint] = useState("http://127.0.0.1:5000");

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
          method: 'POST',
          body: formData
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "API error");

        setAnalysisResult({
          safe: Object.keys(data.prediction)[0] === "No allergens detected",
          allergens: Object.keys(data.prediction),
          confidence: data.confidence || 95,
          rawText: `OCR: ${data.ocr_text || 'N/A'}\n\nTranslated: ${data.translated_text || 'N/A'}`
        });
      } else if (textInput.trim()) {
        const response = await fetch(`${apiEndpoint}/predict`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ingredients: textInput }),
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "API error");

        setAnalysisResult({
          safe: Object.keys(data.prediction)[0] === "No allergens detected",
          allergens: Object.keys(data.prediction),
          confidence: data.confidence || 95,
          rawText: textInput
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
        allergens: offlineDetected.length > 0 ? offlineDetected : ["No allergens detected"],
        confidence: 80,
        rawText: fallbackText
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
          <h1 className="text-3xl font-bold text-gray-900">SafeBite Allergen Detection</h1>
          <p className="text-gray-600 mt-2">Upload image or enter ingredients manually</p>
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
          <label className="block mb-2 font-medium text-gray-700">Upload Image</label>
          <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files[0])} className="mb-4" />

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
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-700'
            }`}
          >
            {isAnalyzing ? (
              <span className="flex items-center justify-center">
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                Analyzing...
              </span>
            ) : (
              'Analyze'
            )}
          </button>
        </div>

        {analysisResult && (
          <div className="bg-white shadow rounded-lg p-6 space-y-4">
            <div className="text-center">
              <div className={`mx-auto flex items-center justify-center h-16 w-16 rounded-full ${
                analysisResult.safe ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {analysisResult.safe ? (
                  <CheckCircle className="h-10 w-10 text-green-600" />
                ) : (
                  <XCircle className="h-10 w-10 text-red-600" />
                )}
              </div>
              <h3 className={`mt-3 text-2xl font-bold ${
                analysisResult.safe ? 'text-green-600' : 'text-red-600'
              }`}>
                {analysisResult.safe ? 'No Allergens Detected' : 'Allergens Found'}
              </h3>
              <p className="text-gray-500">Confidence: {analysisResult.confidence}%</p>
            </div>

            {!analysisResult.safe && (
              <div className="bg-red-50 p-4 rounded-lg">
                <h4 className="font-semibold text-red-800 mb-2">Detected Allergens: </h4>
                <div className="flex flex-wrap gap-2">
                  {analysisResult.allergens.map((allergen, idx) => (
                    <span key={idx} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                      {allergen}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="border-t pt-4">
              <h4 className="font-medium text-gray-800 mb-1">Analyzed Text:</h4>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{analysisResult.rawText}</p>
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
