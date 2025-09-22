from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from CTM.models import Patient, Prescription, MedicationEntry
import pandas as pd
import random
from faker import Faker
import os
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Generates and imports weekly dummy data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        statuses = ["Active-Treatment", "Post-Treatment", "Survivorship", "Chronic Illness", "Palliative Care"]
        sources = ["Ministry of Health", "World Health Organization", "UNRWA", "Turkish Red Crescent"]

        output_dir = "dummy_csv"
        os.makedirs(output_dir, exist_ok=True)

        patients_file = os.path.join(output_dir, "patients.csv")
        prescriptions_file = os.path.join(output_dir, "prescriptions.csv")
        medication_entries_file = os.path.join(output_dir, "medication_entries.csv")

        #المرضى
        if os.path.exists(patients_file):
            existing_patients = pd.read_csv(patients_file)
            last_id = existing_patients["id"].max()
        else:
            existing_patients = pd.DataFrame(columns=["id", "name", "state_desc", "current_status", "therapy_start", "registration_date"])
            last_id = 0

        num_new_patients = random.randint(0, 15)
        new_patients = []
        for i in range(last_id + 1, last_id + 1 + num_new_patients):
            name = fake.name()
            desc = fake.sentence(nb_words=12)
            status = random.choice(statuses)
            therapy_start = fake.date_between(start_date="-1y", end_date="today")
            reg_date = make_aware(fake.date_time_between(start_date=therapy_start))
            new_patients.append([i, name, desc, status, therapy_start, reg_date])

        updated_patients = existing_patients.copy()
        if not updated_patients.empty:
            update_fraction = random.uniform(0.05, 0.3)
            update_indices = updated_patients.sample(frac=update_fraction).index
            for i in update_indices:
                updated_patients.at[i, "current_status"] = random.choice(statuses + ["Deceased"])

        new_patients_df = pd.DataFrame(new_patients, columns=existing_patients.columns)
        merged_df = pd.concat([updated_patients, new_patients_df], ignore_index=True)
        merged_df.to_csv(patients_file, index=False, encoding="utf-8-sig")

        for _, row in merged_df.iterrows():
            if pd.notna(row["id"]):
                Patient.objects.update_or_create(
                    id=int(row["id"]),
                    defaults={
                        "name": row["name"],
                        "state_desc": row["state_desc"],
                        "current_status": row["current_status"],
                        "therapy_start": row["therapy_start"],
                        "registration_date": row["registration_date"],
                    },
                )

        #الوصفات
        if os.path.exists(prescriptions_file):
            prescriptions_df = pd.read_csv(prescriptions_file)
            last_pres_id = prescriptions_df["id"].max()
        else:
            prescriptions_df = pd.DataFrame(columns=["id", "patient_id", "medication_id", "dosage", "frequency_days", "start_date", "end_date"])
            last_pres_id = 0

        num_new_prescriptions = random.randint(0, num_new_patients)
        new_prescriptions = []
        for i in range(num_new_prescriptions):
            pres_id = last_pres_id + 1 + i
            patient_id = last_id + 1 + i
            medication_id = random.randint(1, 5)
            dosage = random.randint(10, 100)
            freq = random.choice([1, 3, 7])
            start_date = fake.date_between(start_date="-1M", end_date="today")
            end_date = start_date + timedelta(days=random.randint(7, 60))
            new_prescriptions.append([pres_id, patient_id, medication_id, dosage, freq, start_date, end_date])

        new_pres_df = pd.DataFrame(new_prescriptions, columns=prescriptions_df.columns)
        prescriptions_df = pd.concat([prescriptions_df, new_pres_df], ignore_index=True)
        prescriptions_df.to_csv(prescriptions_file, index=False, encoding="utf-8-sig")

        new_pres_df = new_pres_df.dropna(subset=["id", "patient_id", "medication_id"])
        new_pres_df = new_pres_df.astype({"id": int, "patient_id": int, "medication_id": int})

        for _, row in new_pres_df.iterrows():
            Prescription.objects.update_or_create(
                id=row["id"],
                defaults={
                    "patient_id": row["patient_id"],
                    "medication_id": row["medication_id"],
                    "dosage": row["dosage"],
                    "frequency_days": row["frequency_days"],
                    "start_date": row["start_date"],
                    "end_date": row["end_date"],
                },
            )

        #الشحنات
        if os.path.exists(medication_entries_file):
            entries_df = pd.read_csv(medication_entries_file)
            last_entry_id = entries_df["id"].max()
        else:
            entries_df = pd.DataFrame(columns=["id", "medication_id", "amount", "entry_date", "source"])
            last_entry_id = 0

        num_new_entries = random.randint(0, 5)
        new_entries = []
        for i in range(num_new_entries):
            entry_id = last_entry_id + 1 + i
            medication_id = random.randint(1, 5)
            amount = random.randint(10, 300)
            entry_date = datetime.today().date()
            source = random.choice(sources)
            new_entries.append([entry_id, medication_id, amount, entry_date, source])

        new_entries_df = pd.DataFrame(new_entries, columns=entries_df.columns)
        entries_df = pd.concat([entries_df, new_entries_df], ignore_index=True)
        entries_df.to_csv(medication_entries_file, index=False, encoding="utf-8-sig")

        new_entries_df = new_entries_df.dropna(subset=["id", "medication_id"])
        new_entries_df = new_entries_df.astype({"id": int, "medication_id": int})

        for _, row in new_entries_df.iterrows():
            MedicationEntry.objects.update_or_create(
                id=row["id"],
                defaults={
                    "medication_id": row["medication_id"],
                    "amount": row["amount"],
                    "entry_date": row["entry_date"],
                    "source": row["source"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Weekly dummy data generated and imported successfully"))
