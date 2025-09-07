from django.http import HttpResponseForbidden
from django.utils.timezone import now
import logging

system_logger = logging.getLogger('filemon')
honeypot_logger = logging.getLogger('honeypot')

def honeypot_view(request):
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    path = request.path
    method = request.method
    headers = dict(request.headers)
    
    honeypot_logger.warning(
        f"HONEYPOT: Acceso sospechoso detectado\n"
        f"IP: {ip}\n"
        f"User-Agent: {user_agent}\n"
        f"Ruta: {path}\n"
        f"Método: {method}\n"
        f"Hora: {now()}\n"
        f"Headers: {headers}"
    )

    return HttpResponseForbidden("Acceso denegado.")
