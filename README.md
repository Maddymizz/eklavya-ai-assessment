# 🎓 Eklavya AI – Educational Content Generation Pipeline

An AI-powered multi-agent system that generates educational content (explanations + MCQs) based on grade level and topic. The system is built using **FastAPI (backend)** and **React (frontend)** with a modular agent-based architecture.

---

## 🚀 Features

- 🧠 AI-generated explanations for any topic
- 📚 Automatic MCQ generation (4 questions per topic)
- 🎯 Interactive quiz UI with instant scoring
- ⚙️ FastAPI backend with modular agent design
- 🌐 React frontend with modern dark UI
- 🔄 Fallback system for API failure handling
- 🧩 Extensible pipeline (Generator → Reviewer → Refiner ready)

---

## 🏗️ System Architecture


Frontend (React)
↓
FastAPI Backend
↓
Generator Agent (LLM / Fallback)
↓
MCQ + Explanation Output
↓
Frontend Quiz UI


---

## 📂 Project Structure


eklavya-ai-assessment/
│
├── backend/
│ ├── main.py
│ ├── agents/
│ │ └── generator.py
│ └── .env
│
├── frontend/
│ ├── src/
│ │ └── App.jsx
│ ├── App.css
│ └── package.json
│
├── venv/
└── README.md


---

## ⚙️ Tech Stack

### Backend
- FastAPI
- Python
- Pydantic
- OpenAI / LLM API (optional)
- dotenv

### Frontend
- React (Vite)
- JavaScript (ES6)
- CSS (Dark UI)

---

## 🔧 Setup Instructions

### 1️⃣ Clone Project
```bash
git clone <your-repo-link>
cd eklavya-ai-assessment
2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows

pip install fastapi uvicorn python-dotenv pydantic openai

Run backend:

uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173
🧪 API Endpoint
POST /generate

Request:

{
  "grade": 5,
  "topic": "solar system"
}

Response:

{
  "explanation": "....",
  "mcqs": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }
  ]
}
🎮 How It Works
User enters grade + topic
Frontend sends request to FastAPI
Generator Agent creates:
Explanation
MCQs
Response is displayed in quiz format
User submits answers and gets score
🔁 Fallback System

If AI API is unavailable:

System automatically switches to fallback MCQ generator
Ensures uninterrupted demo experience
📊 Key Highlights
Modular agent-based architecture
API abstraction layer for LLMs
Production-safe fallback mechanism
Clean UI with interactive quiz scoring
Easily extendable to multi-agent pipelines (Reviewer, Refiner)
🔮 Future Improvements
Reviewer Agent (quality checking)
Refinement Agent (improves content)
Authentication system
Database integration (MongoDB / PostgreSQL)
Deployment on cloud (AWS / Vercel)
👨‍💻 Author

Built by Maddy
AI/ML & Full Stack Developer Project

