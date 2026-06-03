from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import pickle
import numpy as np

app = FastAPI(title="EpiWatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="VIVEK123",
        database="epidemic_db",
        auth_plugin="mysql_native_password"
    )
    return conn

@app.get("/")
def home():
    return {"message": "EpiWatch API is running!"}

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total_patients FROM patients")
    patients = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as total_diagnoses FROM diagnoses")
    diagnoses = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "total_patients": patients["total_patients"],
        "total_diagnoses": diagnoses["total_diagnoses"]
    }

@app.get("/outbreaks")
def get_outbreaks():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.state_name, COUNT(*) as case_count
        FROM diagnoses d
        JOIN patients p ON d.patient_id = p.patient_id
        JOIN states s ON p.state_id = s.state_id
        GROUP BY s.state_name
        ORDER BY case_count DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

@app.get("/predict/{state_id}/{week_num}")
def predict_outbreak(state_id: int, week_num: int):
    with open("../ml/model.pkl", "rb") as f:
        model = pickle.load(f)
    features = np.array([[state_id, week_num, 2024, 100]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    return {
        "state_id": state_id,
        "week_num": week_num,
        "outbreak_predicted": bool(prediction),
        "probability": round(float(probability) * 100, 2)
    }