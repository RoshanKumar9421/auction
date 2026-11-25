import os
import django
from django.test import Client
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_auction.settings')
django.setup()

client = Client()

csv_content = b"name,role,base_price,email\nJohn,100,john@test.com"
f = io.BytesIO(csv_content)
f.name = 'dummy.csv'

response = client.post('/', {
    'action_type': 'new',
    'event_name': 'TestEvent',
    'admin_pin': '1234',
    'team_count': '2',
    'budget': '1000',
    'file_upload': f
})

print(response.status_code)
if response.status_code == 500:
    print(response.content)
