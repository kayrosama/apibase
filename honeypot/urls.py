from django.urls import path
from honeypot import views as honeypot_views

urlpatterns = [
    path('cgi-bin/', honeypot_views.honeypot_view),
    path('admin123/', honeypot_views.honeypot_view),
]
