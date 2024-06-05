from django.urls import path
from .views import CustomRequestLogNumberView

urlpatterns = [
    path('list/', CustomRequestLogNumberView.as_view(), name='list'),
]