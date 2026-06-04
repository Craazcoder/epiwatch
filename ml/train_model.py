import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import pickle
import mysql.connector

print("Connecting to database...")
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="VIVEK123",
    database="epidemic_db",
    auth_plugin="mysql_native_password"
)

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
print(f"Total records loaded: {len(df)}")

avg = df['case_count'].mean()
std = df['case_count'].std()
df['outbreak'] = (df['case_count'] > avg + 0.5 * std).astype(int)
print(f"Outbreak cases: {df['outbreak'].sum()}")
print(f"Non-outbreak cases: {(df['outbreak']==0).sum()}")

np.random.seed(42)
df['case_count_noisy'] = df['case_count'] + np.random.normal(0, df['case_count'].std() * 0.1, len(df))
df['rolling_avg'] = df.groupby('state_id')['case_count'].transform(
    lambda x: x.rolling(window=2, min_periods=1).mean()
)

X = df[['state_id', 'week_num', 'year_num', 'case_count_noisy', 'rolling_avg']]
y = df['outbreak']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)
print(f"\n===== RESULTS =====")
print(f"Test Accuracy: {test_acc * 100:.2f}%")

cv_scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

print(f"\nClassification Report:")
print(classification_report(y_test, y_pred))

print(f"\nFeature Importance:")
for feat, imp in zip(X.columns, model.feature_importances_):
    print(f"  {feat}: {imp:.3f}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("\nModel saved successfully!")