from django.urls import path
from .views import CustomRequestLogListView, CustomRequestLogNumberView

urlpatterns = [
    path('list/', CustomRequestLogListView.as_view(), name='list'),
    path('list-number/', CustomRequestLogNumberView.as_view(), name='list-number'),
]