# 🦠 EpiWatch — Real-time Epidemic Detection Engine

A full-stack data engineering project that monitors real COVID-19 data across WHO regions and predicts future outbreaks using Machine Learning.

## 🔍 What it does
- Stores and analyzes 54,000+ real COVID-19 records from 180+ countries
- Detects disease outbreak patterns using SQL Window Functions
- Predicts outbreak probability using Random Forest ML model
- Displays live charts and predictions on a React dashboard

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Database | MySQL 8.0 |
| Backend API | Python, FastAPI |
| Machine Learning | Scikit-learn, Random Forest |
| Frontend | React.js, Recharts |
| Data Source | WHO COVID-19 Dataset (Kaggle) |

## 📊 Features
- Cases by Region bar chart
- Outbreak Predictor with ML probability
- REST API with auto docs at /docs
- 54,276 real patient and diagnosis records

## 🚀 How to Run

Backend:
cd backend
venv\Scripts\activate
uvicorn main:app --reload

Frontend:
cd frontend
npm run dev

## 📁 Project Structure
epiwatch/
├── backend/          # FastAPI backend + ML API
│   └── main.py       # All API endpoints
├── frontend/         # React dashboard
│   └── src/App.jsx   # Main dashboard component
├── ml/               # Machine Learning
│   ├── train_model.py # Model training script
│   └── model.pkl     # Trained Random Forest model
├── data/             # Data scripts
│   └── load_real_data.py # COVID data loader
└── queries/          # SQL analytics queries

## 👨‍💻 Author
Vivek — https://github.com/Craazcoder
