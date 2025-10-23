# 🧠 Visual Recall Backend

FastAPI backend for the **AI-Powered Visual Recall Journal** — an intelligent memory application that lets users store and search photos, notes, and experiences.

---

## 🚀 Features
- 🧩 User authentication with Firebase
- 🗂️ Upload and manage image memories
- 🔍 Semantic search (image + text-based)
- ⚡ FastAPI with async endpoints
- 🧰 Environment-based configuration using `.env`

---

## 🏗️ Tech Stack
- **Backend:** FastAPI (Python)
- **Auth:** Firebase Admin SDK
- **Database:** (Optional – Firestore / any vector DB)
- **Storage:** Firebase Storage / Cloud Storage
- **Environment:** Python 3.10+  
- **Server:** Uvicorn


## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/visual-recall-backend.git
cd visual-recall-backend
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables
FIREBASE_CREDENTIALS_PATH=path/to/your/firebase-adminsdk.json

▶️ Run the Server
uvicorn app.main:app --reload
