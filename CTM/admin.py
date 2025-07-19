from django.contrib import admin
from .models import Patient, Medication, Prescription, MedicationEntry

# Register your models here.
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(Prescription)
admin.site.register(MedicationEntry)