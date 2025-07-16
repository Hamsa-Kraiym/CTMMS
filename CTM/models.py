from django.db import models

# Create your models here.
class Patient(models.Model):
    #patient_id = models.SmallAutoField()
    name = models.CharField(max_length=100)
    state_desc = models.TextField()
    current_status = models.TextField()
    therapy_start = models.DateField()
    registration_date = models.DateTimeField("date published")

    def __str__(self):
        return self.name + ' (#' + self.id + ') ' 


class Medication(models.Model):
    #medication_id = models.SmallAutoField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name + ' (#' + self.id + ') ' 

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
