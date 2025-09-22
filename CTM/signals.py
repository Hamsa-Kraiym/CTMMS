from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicationEntry, MedicationAmounts, Prescription

@receiver(post_save, sender=MedicationEntry)
def update_medication_amount_on_entry(sender, instance, created, **kwargs):
    """
    When a new MedicationEntry is created, update MedicationAmounts.
    If it doesn't exist, create a new one.
    """
    if created:  # only on new insert, not update
        # Get or create the MedicationAmounts record for this medication
        med_amount, _ = MedicationAmounts.objects.get_or_create(
            medication=instance.medication,
            defaults={"amount": 0, "change_date": instance.entry_date}
        )

        # Increase the amount
        med_amount.amount += instance.amount
        med_amount.change_date = instance.entry_date
        med_amount.save()

@receiver(post_save, sender=Prescription)
def update_medication_amount_on_perscription(sender, instance, created, **kwargs):
    """
    When a new Prescription is created, update MedicationAmounts.
    If it doesn't exist, create a new one.
    """
    if created:  # only on new insert, not update
        # Get or create the MedicationAmounts record for this medication
        med_amount, _ = MedicationAmounts.objects.get_or_create(
            medication=instance.medication,
            defaults={"amount": 0, "change_date": instance.start_date}
        )

        # Increase the amount
        total_days = (instance.end_date - instance.start_date).days + 1  # inclusive of start_date

        # Number of doses in this period
        num_doses = (total_days // instance.frequency_days) + (1 if total_days % instance.frequency_days != 0 else 0)

        med_amount.amount += instance.dosage * num_doses
        med_amount.change_date = instance.start_date
        med_amount.save()