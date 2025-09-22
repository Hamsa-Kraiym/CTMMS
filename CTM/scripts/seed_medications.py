
import sys
sys.path.append("/home/aya/CTMMS")
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTMMS.settings")
django.setup()

from CTM.models import Medication

medications = [
    ("Tamoxifen", "Hormone-receptor-positive breast cancer"),
    ("Cisplatin", "General chemotherapy"),
    ("Rituximab", "Blood cancers (CD20 protein)"),
    ("Fluorouracil", "Colon and stomach cancers"),
    ("Doxorubicin", "Leukemia and solid tumors"),
]

for name, desc in medications:
    Medication.objects.get_or_create(name=name, defaults={"description": desc})

print("Medications seeded")
