import random
from faker import Faker
from django.core.management.base import BaseCommand
from CTM.models import Medication  

class Command(BaseCommand):
    help = "Seed Medication table with cancer-related drugs"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # قائمة أسماء أدوية سرطان مشهورة
        cancer_drugs = [
            "Cisplatin", "Carboplatin", "Oxaliplatin", "Cyclophosphamide",
            "Ifosfamide", "Methotrexate", "5-Fluorouracil", "Capecitabine",
            "Gemcitabine", "Paclitaxel", "Docetaxel", "Vincristine",
            "Vinblastine", "Vinorelbine", "Doxorubicin", "Epirubicin",
            "Daunorubicin", "Idarubicin", "Topotecan", "Irinotecan",
            "Etoposide", "Tamoxifen", "Anastrozole", "Letrozole",
            "Imatinib", "Dasatinib", "Nilotinib", "Trastuzumab",
            "Bevacizumab", "Pembrolizumab", "Nivolumab", "Atezolizumab",
            "Durvalumab", "Ipilimumab", "Olaparib", "Rucaparib",
            "Niraparib", "Talazoparib", "Lenalidomide", "Pomalidomide",
            "Thalidomide", "Sorafenib", "Sunitinib", "Axitinib",
            "Lenvatinib", "Pazopanib", "Regorafenib", "Cabozantinib",
            "Everolimus", "Temsirolimus"
        ]

        # إنشاء 100 سجل
        for _ in range(100):
            drug_name = random.choice(cancer_drugs) + f" {random.randint(1, 500)}mg"
            description = fake.sentence(nb_words=15)

            Medication.objects.create(
                name=drug_name,
                description=description
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 100 cancer medications."))