from django.db import models

class CustomRequestLog(models.Model):
    status = models.CharField(max_length=50)
    successful = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.create_date} - {self.status} - {'Success' if self.successful else 'Failure'}"
