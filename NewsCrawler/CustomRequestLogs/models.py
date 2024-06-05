from django.db import models

class CustomRequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.timestamp} - {self.status} - {'Success' if self.successful else 'Failure'}"
