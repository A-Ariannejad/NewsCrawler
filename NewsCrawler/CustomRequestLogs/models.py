from django.db import models
from CustomUsers.models import CustomUser

class CustomRequestLog(models.Model):
    requested_url = models.CharField(max_length=250)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50)
    successful = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requested_url} - {self.status} - {self.successful}"
