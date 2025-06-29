# 🛡️ SafeBite – AI-Powered Food Allergen Detection

SafeBite is an intelligent food allergen detection system that analyzes ingredient text using machine learning and provides real-time allergen warnings. It integrates Firebase for user authentication and history tracking, making it a reliable companion for individuals with dietary restrictions.

---

## 🚀 Features

- 🧠 **ML-Based Allergen Detection** – Scans ingredient lists for potential allergens using a trained ML model and keyword mapping.
- 🔐 **Firebase Authentication** – Supports email/password and Google sign-in for secure access.
- 📊 **Scan History Tracking** – Logged-in users can view their past analysis with detected allergens.
- ⚡ **Real-Time Result** – Instant feedback with visual indicators for safe or unsafe food items.
- 🌐 **Responsive UI** – Built with React, Vite, and TailwindCSS.
- 🔗 **Firestore Integration** – Stores per-user scan history securely in the cloud.

---

## 📂 Project Structure

hexa-falls/
│
├── flask_backend/
│ ├── app.py # Flask API with ML model + Firebase write
│ ├── firebase_key.json # Firebase Admin SDK key (DO NOT expose publicly)
│ └── model/
│ ├── safebite_model.pkl
│ └── safebite_vectorizer.pkl
│
└── react_frontend/
├── src/
│ ├── assets/components/
│ │ ├── UploadPage.jsx
│ │ ├── HistoryPage.jsx
│ │ └── AuthHero.jsx
│ ├── utils/
│ │ └── firebase.js
│ └── App.jsx
└── package.json

## 🔧 Tech Stack

- **Frontend**: React.js + Vite + TailwindCSS
- **Backend**: Flask + Scikit-learn + Pickle
- **Database**: Firebase Firestore
- **Auth**: Firebase Authentication (Email, Google)
- **Model**: Binary classifier trained on allergen-tagged text data

---

## 🛠️ Setup Instructions

### 1️⃣ Firebase Configuration

1. Create a Firebase project at [firebase.google.com](https://firebase.google.com).
2. Enable Authentication (Email/Password + Google).
3. Set up Firestore in **test mode**.
4. Go to Project Settings → Service accounts → Generate new private key → download as `firebase_key.json`.
5. Place `firebase_key.json` inside `flask_backend/`.

### 2️⃣ Backend Setup (Flask + Model)

bash
cd flask_backend
pip install -r requirements.txt  # flask, firebase-admin, flask-cors, scikit-learn
python app.py  # Starts server at http://127.0.0.1:5000

###3️⃣ Frontend Setup (React + Firebase)

cd react_frontend
npm install
npm run dev  # Runs app at http://localhost:5173

###🔐 Firestore Database Structure

users
 └── {uid}
      └── allergens: [array]
      └── scans
           └── {scanId}
                ├── rawText: string
                ├── allergens: [array]
                ├── safe: boolean
                └── timestamp: serverTimestamp


###🔐 Firestore Security Rules

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}


##🧪 How It Works

User enters food ingredients.
Text is sent to the Flask backend at /predict.
Text is cleaned, vectorized, and passed to a multi-label classifier.
Detected allergens are returned to the frontend.
Results are stored in Firestore under the logged-in user.


##💡 Future Improvements

📷 Image OCR-based ingredient extraction.
🌍 Multi-language allergen detection.
📱 Mobile app integration.
📊 Analytics Dashboard for user scans.


##🧠 Built With

React + Vite + TailwindCSS
Flask + Scikit-learn
Firebase (Auth + Firestore)
Pickle for ML model
Lucide Icons


##✨ Tagline

###Scan It. Know It. Trust Your Bite.


##📃 License

This project is open-source and available under the MIT License.


##🙌 Credits
Developed by Arpan Kundu for the HexaFalls Hackathon.

GitHub: @ARPANkundu2404

Let me know if you'd like:
- Screenshots section with placeholders
- README badges (e.g., build passing, license)
- Deployment instructions for Render / Firebase Hosting / Vercel

Good luck with your hackathon demo! 🏆


