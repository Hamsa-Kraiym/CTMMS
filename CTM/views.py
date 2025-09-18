from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Patient

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def dashboard(request):
    totalNo = Patient.total_patients()
    return render(request, "dashboard.html", {
        "totalNo": totalNo,
        "total_title": "Total Patients", 
        "change_percent" : 3.2,
        "up_down_arrow" : "up" ,
        "change_note" : "Since Last Month"
    })
