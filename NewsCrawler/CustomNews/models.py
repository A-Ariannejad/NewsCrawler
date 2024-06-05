from django.db import models

class CustomNew(models.Model):
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    yjc_id = models.CharField(unique=True, max_length=10)
    pubDate_ad = models.DateTimeField()
    pubDate_solar = models.DateTimeField()
    description = models.TextField(max_length=250, null=True, blank=True)
    STATUS_TYPE = (
        ('latest', 'latest'),
        ('most_visited', 'most_visited'),
    )
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='latest')
    create_date = models.DateTimeField(auto_now_add=True)