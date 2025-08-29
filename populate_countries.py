
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ultras.settings')  
django.setup()

from main.models import Country  

json_file_path = os.path.join(os.path.dirname(__file__), 'main', 'data', 'countries.json')

with open(json_file_path, 'r', encoding='utf-8') as f:
    countries = json.load(f)

for country_name in countries:
    country_name = country_name.get('name') if isinstance(country_name, dict) else country_name
    if country_name:
        Country.objects.get_or_create(name=country_name)

print(f"{len(countries)} countries added to the database.")
