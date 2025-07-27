import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
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
        response = requests.post(
            'http://127.0.0.1:8000/apis/auth/login',
            json={'email': email, 'password': password}
        )

        print("Respuesta de la API:", response.text)

        if response.status_code == 200:
            token = response.json().get('access')
            if token:
                response = redirect('/menu/')  # Ajusta esta ruta según tu menú
                response.set_cookie('auth_token', token)
                return response
            else:
                return render(request, 'frontend/login.html', {'error': 'Token no recibido.'})
        else:
            return render(request, 'frontend/login.html', {'error': 'Correo o contraseña incorrectos.'})

    return render(request, 'frontend/login.html')

def menu_view(request):
    return render(request, 'frontend/menu.html')

def home_view(request):
    return render(request, 'frontend/home.html')

def reports_view(request):
    return render(request, 'frontend/reports.html')

def about_view(request):
    return render(request, 'frontend/about.html')

