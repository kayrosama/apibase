# frontend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('track/', views.track_view, name='track'),
    path('ship/', views.ship_view, name='ship'),
    path('about/', views.about_view, name='about'),
    path('logout/', views.logout_view, name='logout'),
    ]

