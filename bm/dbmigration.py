import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bm.settings')

from django.core.management import call_command
with open('bmapp/models.py', 'w', encoding='utf-8') as f:
    call_command('inspectdb', stdout=f)