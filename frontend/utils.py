import requests

def is_token_valid(token):
    if not token:
        return False

    try:
        response = requests.post(
            'http://127.0.0.1:8000/apis/auth/verify',
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.status_code == 200
    except requests.RequestException:
        return False
        
