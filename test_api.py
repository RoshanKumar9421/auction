import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_auction.settings')
django.setup()

client = Client()

response = client.get('/api/state/')
print("Status:", response.status_code)
if response.status_code == 500:
    print(response.content)
