from django.contrib import admin
from .models import Patient, Medication, Prescription, MedicationEntry

admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(Prescription)
admin.site.register(MedicationEntry)
