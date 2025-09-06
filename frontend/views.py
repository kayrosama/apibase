import requests
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core_auth.decorators import token_required
from core_auth.utils import is_token_valid
from core_auth.config import get_endpoint


@csrf_exempt
def login_view(request):
    token = request.COOKIES.get('auth_token')
    if is_token_valid(token):
        return redirect('/track/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validaciones básicas
        if not email:
            return render(request, 'frontend/login.html', {'error': 'Por favor, ingresa tu correo electrónico.'})
        if not password:
            return render(request, 'frontend/login.html', {'error': 'Por favor, ingresa tu contraseña.'})
        if len(password) < 6:
            return render(request, 'frontend/login.html', {'error': 'La contraseña debe tener al menos 6 caracteres.'})

        # Llamada a la API
        url = get_endpoint('auth_login')
        response = requests.post(
            url, 
            json={'email': email, 'password': password}
        )

        print("Respuesta de la API:", response.text)

        if response.status_code == 200:
            token = response.json().get('access')
            if token:
                response = redirect('/track/')  # Ajusta esta ruta según tu menú
                response.set_cookie('auth_token', token)
                return response
            else:
                return render(request, 'frontend/login.html', {'error': 'Token no recibido.'})
        else:
            return render(request, 'frontend/login.html', {'error': 'Correo o contraseña incorrectos.'})

    return render(request, 'frontend/login.html')


@token_required
def track_view(request):
    return render(request, 'frontend/tracking.html')

@token_required
def ship_view(request):
    return render(request, 'frontend/shipping.html')

@token_required
def about_view(request):
    return render(request, 'frontend/about.html')

def logout_view(request):
    logout(request)
    response = redirect('login') 
    response.delete_cookie('auth_token') 
    return response


