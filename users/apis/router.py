from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apis.views import RegisterView, UserView, VerifyTokenView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='user-register'),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/verify', VerifyTokenView.as_view(), name='verify-token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/mante', UserView.as_view(), name='user-detail'),  # Soporta ?id= y ?all_users=
]

