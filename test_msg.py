import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_auction.settings')
django.setup()

client = Client()

# trigger an exception in the view by uploading a text file (not csv/xlsx)
# wait, if I upload a .txt file, it will fall into `else: df = pd.read_excel(f)`
# and openpyxl will raise an error.
# Let's see what happens.
with open("requirements.txt", "rb") as f:
    response = client.post('/', {
        'action_type': 'new',
        'event_name': 'TestEventError',
        'admin_pin': '1234',
        'team_count': '2',
        'budget': '1000',
        'file_upload': f
    })

print(response.status_code)
if response.status_code == 500:
    print(response.content)
