
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
import json
import calendar

from CTM.models import Patient , MedicationEntry, MedicationAmounts

def calculate_change_rate(old_value, new_value):
    """
    Calculate percentage change rate between old and new values.

    Args:
        old_value (int|float): The previous period value.
        new_value (int|float): The current period value.

    Returns:
        float | None: Change rate (%) or None if old_value = 0.
    """
    if old_value == 0:
        if new_value == 0:
            return 0.0   # no change
        else:
            return 100.0  # or return 100.0 to indicate full growth
    return round(((new_value - old_value) / old_value) * 100 , 2)

def get_new_registered_patients_6months():
    
    today = now().date()
    six_months_ago = today.replace(day=1) - timedelta(days=180)

    # Group patients by month of registration
    monthly_data = (
        Patient.objects.filter(registration_date__date__gte=six_months_ago)
        .annotate(month=TruncMonth("registration_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    # Prepare chart labels and values
    labels = []
    data = []

    # Ensure all 6 months are included (even if count = 0)
    for i in range(6, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month_name = calendar.month_abbr[month_date.month]  # e.g. 'Sep'
        labels.append(month_name)

        # get count if exists, else 0
        month_count = next((item["count"] for item in monthly_data if item["month"].month == month_date.month), 0)
        data.append(month_count)

    return {
        "labels": labels,
        "datasets": [{
            "label": "New Patients",
            "data": data
        }]
    }

def get_medications_entries_6months():
    today = now().date()
    six_months_ago = today - timedelta(days=180)

    # Aggregate entries by month
    entries = (
        MedicationEntry.objects.filter(entry_date__gte=six_months_ago)
        .annotate(month=TruncMonth("entry_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    labels = []
    data = []

    for entry in entries:
        month_name = calendar.month_abbr[entry["month"].month]  # 'Jul', 'Aug', ...
        labels.append(month_name)
        data.append(entry["total"] or 0)

    return {
        "labels": labels,
        "datasets": [{
            "label": "Shipments",
            "data": data
        }]
    }