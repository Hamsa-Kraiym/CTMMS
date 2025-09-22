from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from . import views

path('', lambda request: redirect('admin/')),


urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard", views.dashboard, name="dashboard"),
    path('medic_amounts', views.availablity_report, name="availablity_report"),
    path("", views.dashboard, name="index")
]
