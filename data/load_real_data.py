import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="VIVEK123",
    database="epidemic_db",
    auth_plugin="mysql_native_password"
)
cursor = conn.cursor()

# Insert WHO Regions as states
df = pd.read_csv("full_grouped.csv")
regions = df['WHO Region'].dropna().unique().tolist()
for r in regions:
    cursor.execute("INSERT INTO states (state_name, region) VALUES (%s, %s)", (r, r))
conn.commit()
print("Regions inserted!")

# Insert diseases
diseases = [("COVID-19","Viral",True)]
for d in diseases:
    cursor.execute("INSERT INTO diseases (disease_name, category, is_epidemic_prone) VALUES (%s,%s,%s)", d)
conn.commit()
print("Disease inserted!")

# Insert countries as hospitals
countries = df['Country/Region'].dropna().unique().tolist()
for i, c in enumerate(countries):
    state_id = (i % len(regions)) + 1
    cursor.execute("INSERT INTO hospitals (hospital_name, state_id, capacity) VALUES (%s,%s,%s)",
                   (c, state_id, 1000))
conn.commit()
print("Countries/Hospitals inserted!")

# Insert patient and diagnosis records from real data
batch_patients = []
batch_diagnoses = []
count = 0

for _, row in df.iterrows():
    confirmed = int(row['Confirmed']) if pd.notna(row['Confirmed']) else 0
    if confirmed == 0:
        continue
    adm_date = row['Date']
    state_id = (list(regions).index(row['WHO Region']) + 1) if pd.notna(row['WHO Region']) else 1
    hospital_id = (list(countries).index(row['Country/Region']) + 1) if row['Country/Region'] in countries else 1

    cursor.execute(
        "INSERT INTO patients (age, gender, state_id, admission_date) VALUES (%s,%s,%s,%s)",
        (30, 'M', state_id, adm_date))
    patient_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO diagnoses (patient_id, disease_id, hospital_id, diagnosis_date) VALUES (%s,%s,%s,%s)",
        (patient_id, 1, hospital_id, adm_date))
    count += 1
    if count % 1000 == 0:
        conn.commit()
        print(f"Inserted {count} records...")

conn.commit()
print(f"Done! Total records: {count}")
cursor.close()
conn.close()