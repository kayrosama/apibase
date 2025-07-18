import flet as ft
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

API_URL = "http://127.0.0.1:8000/apis/auth/login"

def main(page: ft.Page):
    page.title = "Mi App"
    page.theme_mode = "light"
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(login_view())
        elif page.route == "/dashboard":
            page.views.append(dashboard_view())
        
        page.update()
        
    def login_view():
        username = ft.TextField(label="Usuario", width=300)
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        mensaje = ft.Text()
        
        def login(e):
            response = requests.post(API_URL, json={"email": username.value, "password": password.value})
            
            if response.status_code == 200:
                token = response.json().get("access")
                page.client_storage.set("token", token)
                page.go("/dashboard")
            else:
                mensaje.value = "Credenciales incorrectas"
                mensaje.color = "red"
                page.update()
                
        return ft.View(
            route="/",
            controls=[
                ft.Column([
                    ft.Text("Iniciar Sesión", size=30, weight="bold"),
                    username,
                    password,
                    ft.ElevatedButton("Ingresar", on_click=login),
                    mensaje
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        
    def dashboard_view():
        return ft.View(
            route="/dashboard",
            controls=[
                ft.Text("Bienvenido al panel principal", size=25),
                ft.Row([
                    ft.ElevatedButton("Opción 1", on_click=lambda e: print("Opción 1")),
                    ft.ElevatedButton("Opción 2", on_click=lambda e: print("Opción 2")),
                    ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.go("/"))
                ])
            ]
        )
        
    page.on_route_change = route_change
    page.go(page.route)
    
ft.app(target=main, view=ft.WEB_BROWSER)

