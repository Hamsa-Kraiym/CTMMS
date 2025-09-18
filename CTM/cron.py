
from django_cron import CronJobBase, Schedule
import subprocess
import os

class WeeklyDataGenerator(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7  # مرة كل أسبوع

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CTM.weekly_data_generator'  # كود مميز للمهمة

    def do(self):
        script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'generate_weekly_data.py')
        subprocess.run(['python3', script_path], check=True)
