from functools import wraps
from django.shortcuts import redirect
from .utils import is_token_valid

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if not is_token_valid(token):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    
