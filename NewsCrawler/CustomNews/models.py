from django.db import models

class CustomNew(models.Model):
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    yjc_id = models.IntegerField()
    pubDate_ad = models.DateTimeField()
    pubDate_solar = models.DateTimeField()
    description = models.TextField(max_length=250, null=True, blank=True)
    STATUS_TYPE = (
        ('latest', 'service'),
        ('most_visited', 'person_to_site'),
    )
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='latest')
    create_date = models.DateTimeField(auto_now_add=True)