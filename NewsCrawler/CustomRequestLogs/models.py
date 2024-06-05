from django.db import models

class CustomRequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.timestamp} - {'Success' if self.status else 'Failure'}"
