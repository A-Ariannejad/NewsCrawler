from django.db import models

class CustomNew(models.Model):
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    yjc_id = models.IntegerField()
    pubDate_ad = models.DateTimeField()
    pubDate_solar = models.DateTimeField()
    description = models.TextField(max_length=250, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)