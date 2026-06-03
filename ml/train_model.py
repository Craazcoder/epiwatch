import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="VIVEK123",
    database="epidemic_db",
    auth_plugin="mysql_native_password"
)

# Pull data from MySQL
query = """
    SELECT p.state_id, COUNT(*) as case_count,
    WEEK(d.diagnosis_date) as week_num,
    YEAR(d.diagnosis_date) as year_num
    FROM diagnoses d
    JOIN patients p ON d.patient_id = p.patient_id
    GROUP BY p.state_id, week_num, year_num
"""
df = pd.read_sql(query, conn)
conn.close()

# Create outbreak label (1 if cases > average)
avg = df['case_count'].mean()
df['outbreak'] = (df['case_count'] > avg).astype(int)

# Features and target
X = df[['state_id', 'week_num', 'year_num', 'case_count']]
y = df['outbreak']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Accuracy
acc = accuracy_score(y_test, model.predict(X_test))
print(f"Model Accuracy: {acc * 100:.2f}%")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved!")