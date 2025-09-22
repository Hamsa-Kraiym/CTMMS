from django.db import models
from django.db.models import Count
from django.utils.timezone import now

# Create your models here.
class Patient(models.Model):
    #patient_id = models.SmallAutoField()
    name = models.CharField(max_length=100)
    state_desc = models.TextField()
    current_status = models.TextField()
    therapy_start = models.DateField()
    registration_date = models.DateTimeField("date published")

    def __str__(self):
        return self.name + ' (#' + str(self.id) + ') '

    @classmethod
    def total_patients(cls):
        return cls.objects.count()
    
    @classmethod
    def total_patients_by_status(cls):
        return cls.objects.values("current_status").annotate(total=Count("id"))


class Medication(models.Model):
    #medication_id = models.SmallAutoField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name + ' (#' + str(self.id) + ') ' 
    
    @classmethod
    def unavailability_report(cls):
        """
        Returns a list of medications with:
        - number of patients using it
        - total required amount
        - available amount
        - unavailability rate %
        Ordered by unavailability rate (descending)
        """
        data = []

        for med in cls.objects.all():
            # Count patients using this medication
            patients_count = (
                Prescription.objects.filter(medication=med)
                .values("patient")
                .distinct()
                .count()
            )

            if patients_count == 0:
                continue  # skip unused medications

            # Calculate total required (demand) from prescriptions
            total_required = 0
            prescriptions = Prescription.objects.filter(medication=med)
            for p in prescriptions:
                total_days = (p.end_date - p.start_date).days + 1
                num_doses = (total_days // p.frequency_days) + (1 if total_days % p.frequency_days != 0 else 0)
                total_required += p.dosage * num_doses

            if total_required == 0:
                continue

            # Available stock (last record from MedicationAmounts)
            available_record = MedicationAmounts.objects.filter(medication=med).last()
            available_amount = available_record.amount if available_record else 0

            # Calculate unavailability rate
            availability_rate = (available_amount / total_required * 100) if total_required > 0 else 0
            unavailability_rate = 100 - availability_rate

            data.append({
                "medication": med.name,
                "patients": patients_count,
                "required": total_required,
                "available": available_amount,
                "unavailability_rate": round(unavailability_rate, 1),
            })

        # Order by unavailability rate (highest first)
        return sorted(data, key=lambda x: x["unavailability_rate"], reverse=True)
    
    @classmethod
    def availability_report(cls):
        """
        Returns a list of medications with:
        - number of patients using it
        - total required amount (demand)
        - available amount (stock)
        - availability rate %
        """
        data = []
        for med in cls.objects.all():
            # Patients using this med
            patients_count = Prescription.objects.filter(medication=med).values("patient").distinct().count()

            # Required stock
            total_required = 0
            for p in Prescription.objects.filter(medication=med):
                total_days = (p.end_date - p.start_date).days + 1
                num_doses = (total_days // p.frequency_days) + (1 if total_days % p.frequency_days != 0 else 0)
                total_required += p.dosage * num_doses

            # Available stock (from MedicationAmounts)
            available = MedicationAmounts.objects.filter(medication=med).last()
            available_amount = available.amount if available else 0

            # Availability rate
            availability_rate = round(available_amount / total_required * 100, 1) if total_required > 0 else "-"

            data.append({
                "medication": med.name,
                "patients": patients_count,
                "required": total_required,
                "available": available_amount,
                "availability_rate": availability_rate
            })

        return data

class Prescription(models.Model):
    #prescription_id = models.SmallAutoField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    dosage = models.SmallIntegerField()
    frequency_days = models.SmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

class MedicationEntry(models.Model):
    #entry_id = models.SmallAutoField()
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()
    entry_date = models.DateField()
    source = models.CharField(max_length=200)

    @classmethod
    def total_medication_entries(cls):
        return cls.objects.count()
    
class MedicationAmounts(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    amount = models.IntegerField()
    change_date = models.DateField()

    @classmethod
    def unavailable_medications(cls):
        return cls.objects.filter(amount__lte=0).count()
