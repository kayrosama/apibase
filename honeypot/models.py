from django.db import models


class SystemOutLog(models.Model):
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    headers = models.JSONField()

