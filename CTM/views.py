from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
import json
import calendar
from .models import Patient , Medication, MedicationEntry, MedicationAmounts, Prescription
from .utility.functions import *

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def dashboard(request):
    ptotalNo = Patient.total_patients()
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    prev_month = today - timedelta(days=60)

    new_patiants = Patient.objects.filter(registration_date__gte=last_month).count()
    old_patiants = Patient.objects.filter(registration_date__gte=prev_month, registration_date__lt=last_month).count()
    patient_change = calculate_change_rate(old_patiants, new_patiants)

    etotalNo = MedicationEntry.total_medication_entries()
    new_entries = MedicationEntry.objects.filter(entry_date__gte=last_month).count()
    old_entries = MedicationEntry.objects.filter(entry_date__gte=prev_month, entry_date__lt=last_month).count()
    entry_change = calculate_change_rate(old_entries, new_entries)

    htotal = Patient.total_patients_by_status()
    htotalNo = next(
        (item["total"] for item in htotal if item["current_status"] == "Survivorship"),
        0  # default if not found
    )
    new_heald = Patient.objects.filter(registration_date__gte=last_month, current_status="Survivorship").count()
    old_heald = Patient.objects.filter(registration_date__gte=prev_month, registration_date__lt=last_month, current_status="Survivorship").count()
    heald_change = calculate_change_rate(old_heald, new_heald)

    stotalNo = MedicationAmounts.unavailable_medications()
    new_short = MedicationAmounts.objects.filter(change_date__gte=last_month, amount__lte=0).count()
    old_short = MedicationAmounts.objects.filter(change_date__gte=prev_month, change_date__lt=last_month, amount__lte=0).count()
    print("DEBUG >>> last_month:", last_month) 
    short_change = calculate_change_rate(old_short, new_short)

    patients_chart_data = get_new_registered_patients_6months()
    entries_bars_data = get_medications_entries_6months()

    return render(request, "dashboard.html", {
        "ptotalNo": ptotalNo,
        "pchange_percent" : patient_change,
        "p_up_down_arrow" : "up" if patient_change >=0 else "down" ,
        "p_arrow_color" : "success" if patient_change >=0 else "danger" ,
        "change_note" : "Since Last Month",

        "etotalNo": etotalNo,
        "echange_percent" : entry_change,
        "e_up_down_arrow" : "up" if entry_change >=0 else "down" ,
        "e_arrow_color" : "success" if entry_change >=0 else "danger" , 

        "htotalNo": htotalNo,
        "hchange_percent" : heald_change,
        "h_up_down_arrow" : "up" if heald_change >=0 else "down" ,
        "h_arrow_color" : "success" if heald_change >=0 else "danger" ,

        "stotalNo": stotalNo,
        "schange_percent" : short_change,
        "s_up_down_arrow" : "up" if short_change >=0 else "down" , 
        "s_arrow_color" : "success" if short_change >=0 else "danger" ,

        "patients_chart" : json.dumps(patients_chart_data),
        "entries_bars" : json.dumps(entries_bars_data), 

        "mentries_details" : MedicationEntry.objects.select_related("medication").order_by("-entry_date")[:50],
        "medications_deficit": Medication.unavailability_report()[:50], 
    })

def availablity_report(request):
    return render(request, "report.html", {"medications_list":Medication.availability_report()})