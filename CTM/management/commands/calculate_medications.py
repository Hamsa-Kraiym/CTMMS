# management/commands/recalc_medications.py
from django.db import models
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from CTM.models import Medication, MedicationEntry, Prescription , MedicationAmounts

class Command(BaseCommand):
    help = "Recalculate and populate MedicationAmounts for all medications"

    def handle(self, *args, **kwargs):
        for med in Medication.objects.all():
            self.calc_medication_amounts(med)
        self.stdout.write(self.style.SUCCESS("MedicationAmounts table updated."))

    def calc_medication_amounts(self, medication):
        # Total entered (stock in)
        total_entries = (
            MedicationEntry.objects.filter(medication=medication)
            .aggregate(total=models.Sum("amount"))["total"]
            or 0
        )

        # Total required (stock out by prescriptions)
        total_required = 0
        prescriptions = Prescription.objects.filter(medication=medication)
        for p in prescriptions:
            total_days = (p.end_date - p.start_date).days + 1 
            num_doses = (total_days // p.frequency_days) + (1 if total_days % p.frequency_days != 0 else 0)
            total_required += p.dosage * num_doses

        # Net available
        net_amount = total_entries - total_required

        # Update or create record in MedicationAmounts
        MedicationAmounts.objects.update_or_create(
            medication=medication,
            defaults={"amount": net_amount, "change_date": now().date()},
        )