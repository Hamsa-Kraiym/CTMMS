from django.contrib import admin
from .models import Patient, Medication, Prescription, MedicationEntry
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(Prescription)

# Use ImportExportModelAdmin for MedicationEntry
@admin.register(MedicationEntry)
class MedicationEntryAdmin(ImportExportModelAdmin):
    pass