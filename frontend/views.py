import logging
import requests
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

logging.basicConfig(level=logging.DEBUG)

@csrf_protect
def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        auth_response = requests.post('http://127.0.0.1:8000/apis/auth/login', data={
            'email': email,
            'password': password
        })
        if auth_response.status_code == 200:
            token = auth_response.json().get('access')
            user_response = requests.get('http://127.0.0.1:8000/apis/auth/mante', headers={
                'Authorization': f'Bearer {token}'
            })
            if user_response.status_code == 200:
                response = redirect('bienvenida')
                response.set_cookie('access_token', token, httponly=True, secure=True, samesite='Lax')
                response.set_cookie('user_data', user_response.text, secure=True, samesite='Lax')
                return response
            else:
                error = 'No se pudieron obtener los datos del usuario'
        else:
            error = 'Credenciales inválidas'
    return render(request, 'frontend/login.html', {'error': error})

def bienvenida(request):
    user_data = request.COOKIES.get('user_data')
    if not user_data:
        return redirect('login')
    user = json.loads(user_data)
    return render(request, 'frontend/bienvenida.html', {'user': user})
