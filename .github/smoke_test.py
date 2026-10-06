# Checks that the backend starts and its APIs answer, without signing in.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'casdoor_django_js_sdk_example.settings')

import django

django.setup()

from django.core.management import call_command
from django.test import Client

call_command('check')
call_command('migrate', verbosity=0)

client = Client(HTTP_HOST='localhost')

response = client.get('/api/get-account')
assert response.json()['status'] == 'error', response.content

response = client.get('/toLogin')
assert b'/login/oauth/authorize?client_id=' in response.content, response.content

response = client.post('/api/signin?code=invalid&state=state')
assert response.json()['status'] == 'error', response.content

response = client.post('/api/signout')
assert response.json()['status'] == 'ok', response.content

print('ok')
