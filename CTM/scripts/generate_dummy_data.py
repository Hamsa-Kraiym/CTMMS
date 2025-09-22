import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()


output_dir = "dummy_csv"
os.makedirs(output_dir, exist_ok=True)


patients_file = os.path.join(output_dir, "patients.csv")
medications_file = os.path.join(output_dir, "medications.csv")
prescriptions_file = os.path.join(output_dir, "prescriptions.csv")
medication_entries_file = os.path.join(output_dir, "medication_entries.csv")


statuses = ["Stable", "Critical", "Improving", "Deteriorating"]
sources = ["Ministry of Health", "International Aid", "UNRWA", "Turkish Red Crescent"]


patients = []
with open(patients_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "state_desc", "current_status", "therapy_start", "registration_date"])
    for i in range(1, 101):
        name = fake.name()
        desc = fake.sentence(nb_words=12)
        status = random.choice(statuses)
        therapy_start = fake.date_between(start_date="-2y", end_date="today")
        reg_date = fake.date_time_between(start_date=therapy_start)
        writer.writerow([i, name, desc, status, therapy_start, reg_date])
        patients.append(i)


medications = [
    (1, "Tamoxifen", "Hormone-receptor-positive breast cancer"),
    (2, "Cisplatin", "General chemotherapy"),
    (3, "Rituximab", "Blood cancers (CD20 protein)"),
    (4, "Fluorouracil", "Colon and stomach cancers"),
    (5, "Doxorubicin", "Leukemia and solid tumors"),
]

with open(medications_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "description"])
    for med in medications:
        writer.writerow(med)


with open(prescriptions_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "patient_id", "medication_id", "dosage", "frequency_days", "start_date", "end_date"])
    for i in range(1, 201):
        patient_id = random.choice(patients)
        medication_id = random.randint(1, 5)
        dosage = random.randint(10, 100)
        freq = random.choice([1, 3, 7])
        start_date = fake.date_between(start_date="-6M", end_date="today")
        end_date = start_date + timedelta(days=random.randint(7, 90))
        writer.writerow([i, patient_id, medication_id, dosage, freq, start_date, end_date])


with open(medication_entries_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "medication_id", "amount", "entry_date", "source"])
    for i in range(1, 61):
        medication_id = random.randint(1, 5)
        amount = random.randint(10, 300)
        entry_date = fake.date_between(start_date="-6M", end_date="today")
        source = random.choice(sources)
        writer.writerow([i, medication_id, amount, entry_date, source])

print("Dummy CSV files generated in folder: dummy_csv")
