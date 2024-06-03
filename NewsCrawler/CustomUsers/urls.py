from django.urls import path, include
from rest_framework import routers
from .views import LoginView

router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('login', LoginView.as_view(), name='token'),
]