from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


path('', lambda request: redirect('admin/')),


urlpatterns = [
    path('admin/', admin.site.urls),
]
