from django.urls import path
from .views import CustomRequestLogListView

urlpatterns = [
    path('list/', CustomRequestLogListView.as_view(), name='list'),
]