import json
import os
from django.conf import settings

def get_endpoint(name):
    path = os.path.join(settings.BASE_DIR, 'static', 'json', 'endpoints.json')
    with open(path, 'r') as f:
        endpoints = json.load(f)
    return endpoints.get(name)

def get_owner(name):
    path = os.path.join(settings.BASE_DIR, 'static', 'json', 'owner.json')
    with open(path, 'r') as f:
        endpoints = json.load(f)
    return endpoints.get(name)

