from django.urls import path
from .views import CustomNewListView

urlpatterns = [
    path('list/', CustomNewListView.as_view(), name='list'),
]