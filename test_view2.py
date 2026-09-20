import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_auction.settings')
django.setup()

client = Client()

with open("dummy.xlsx", "rb") as f:
    response = client.post('/', {
        'action_type': 'new',
        'event_name': 'TestEvent2',
        'admin_pin': '1234',
        'team_count': '2',
        'budget': '1000',
        'file_upload': f
    })

print(response.status_code)
if response.status_code == 500:
    print(response.content)
