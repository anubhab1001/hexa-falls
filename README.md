# 🛡️ SafeBite – AI-Powered Food Allergen Detection

**SafeBite** is an intelligent food allergen detection platform that analyzes ingredient text using machine learning and provides real-time allergen warnings. With Firebase authentication and secure cloud history tracking, SafeBite is a reliable companion for individuals with dietary restrictions.

🌐 **Live Demo:** [safebite-hexafalls.onrender.com](https://safebite-hexafalls.onrender.com/)

---

## 🚀 Features

- 🧠 **ML-Based Allergen Detection:** Scans ingredient lists for potential allergens using a trained machine learning model and keyword mapping.
- 🔐 **Secure Authentication:** Login with email/password or Google via Firebase Authentication.
- 📊 **Personal Scan History:** Logged-in users can view their past analyses with detected allergens, stored securely in Firestore.
- ⚡ **Real-Time Results:** Get instant feedback and visual indicators for safe or unsafe food items.
- 🌐 **Responsive UI:** Modern, mobile-friendly interface built with React, Vite, and TailwindCSS.
- 🔗 **Cloud Storage:** User scan data is stored per-user in Firebase Firestore for privacy and accessibility.

---

## 🔧 Tech Stack

- **Frontend:** React.js + Vite + TailwindCSS
- **Backend:** Flask + Scikit-learn + Pickle
- **Database:** Firebase Firestore
- **Authentication:** Firebase Auth (Email, Google)
- **ML Model:** Binary classifier trained on allergen-tagged ingredient text

---

## 🛠️ Setup Instructions

### 1️⃣ Firebase Configuration

1. Create a Firebase project at [firebase.google.com](https://firebase.google.com).
2. Enable Authentication (Email/Password and Google).
3. Set up Firestore in **test mode**.
4. Go to **Project Settings → Service accounts → Generate new private key** and download as `firebase_key.json`.
5. Place `firebase_key.json` inside `flask_backend/` (never commit this file).

**Important:**  
After deployment, add your deployed frontend domain (e.g., `safebite-hexafalls.onrender.com`) to the **Authorized domains** in Firebase Console → Authentication → Settings.

---

## 🧪 How It Works

1. User enters or uploads food ingredients.
2. Text is sent to the Flask backend at `/predict`.
3. The backend cleans, vectorizes, and classifies the text with the ML model.
4. Detected allergens are returned to the frontend.
5. Results are stored in Firestore under the logged-in user’s history.

---

## 💡 Future Improvements

- 📷 Image OCR-based ingredient extraction
- 🌍 Multi-language allergen detection
- 📱 Mobile app integration
- 📊 Analytics dashboard for user scans

---

## 🧠 Built With

- React + Vite + TailwindCSS
- Flask + Scikit-learn
- Firebase (Auth + Firestore)
- Pickle for ML model
- Lucide Icons

---

## ✨ Tagline

**Scan It. Know It. Trust Your Bite.**

---

## 📃 License

This project is open-source and available under the MIT License.

---

## 🙌 Credits

Developed by Arpan Kundu for the HexaFalls Hackathon.

GitHub: [@ARPANkundu2404](https://github.com/ARPANkundu2404)

---

*For screenshots, badges, or additional deployment instructions (Firebase Hosting, Vercel, etc.), open an issue or PR!*

*Good luck with your hackathon demo! 🏆*





