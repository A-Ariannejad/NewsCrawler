from django.apps import AppConfig


class CustomnewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CustomNews'

    def ready(self):
        from Crawlers.tasks import start_periodic_task  
        start_periodic_task()
