import requests
from core_auth.config import get_endpoint 

def is_token_valid(token):
    if not token:
        return False

    try:
        url = get_endpoint('auth_verify')
        response = requests.post(
            url, 
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

