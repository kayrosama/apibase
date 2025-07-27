# frontend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('home/', views.home_view, name='home'),
    path('reports/', views.reports_view, name='reports'),
    path('about/', views.about_view, name='about'),
    ]

