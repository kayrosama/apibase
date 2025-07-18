
from django.urls import path
from .views import login_view, bienvenida

urlpatterns = [
    path('login/', login_view, name='login'),
    path('bienvenida/', bienvenida, name='bienvenida'),
]
