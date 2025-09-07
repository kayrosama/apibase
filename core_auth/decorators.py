from functools import wraps
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from core_auth.utils import is_token_valid
import logging

logger = logging.getLogger('filemon')

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if not is_token_valid(token):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_permission(required_roles, allow_self=False, restrict_role_change=True):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            target_user_id = request.data.get('id') or kwargs.get('pk')

            if user.role not in required_roles:
                return Response({'detail': 'Acceso denegado por rol'}, status=status.HTTP_403_FORBIDDEN)

            if not allow_self and str(user.id) == str(target_user_id):
                return Response({'detail': 'No puedes modificarte a ti mismo'}, status=status.HTTP_403_FORBIDDEN)

            if restrict_role_change and str(user.id) == str(target_user_id) and 'role' in request.data:
                return Response({'detail': 'No puedes modificar tu propio rol'}, status=status.HTTP_403_FORBIDDEN)

            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def rate_limit_log(key='ip', rate='5/m', block=True):
    def decorator(view_func):
        @method_decorator(ratelimit(key=key, rate=rate, block=block))
        def _wrapped_view(self, request, *args, **kwargs):
            if hasattr(request, 'limited') and request.limited:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
                path = request.path
                logger.warning(f'Rate limit excedido: IP={ip}, PATH={path}')
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator

