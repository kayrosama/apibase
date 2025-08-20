from functools import wraps
from django.shortcuts import redirect
import requests

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if not token:
            return redirect('login')

        # Validar el token contra la API
        try:
            response = requests.post(
                'http://127.0.0.1:8000/apis/auth/verify',
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.status_code != 200:
                return redirect('login')
        except requests.RequestException:
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

