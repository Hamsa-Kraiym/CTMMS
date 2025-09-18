from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from . import views

path('', lambda request: redirect('admin/')),


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
]
