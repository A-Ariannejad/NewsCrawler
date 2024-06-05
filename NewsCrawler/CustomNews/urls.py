from django.urls import path
from .views import CustomNewListView, CustomNewShowView

urlpatterns = [
    path('show/<int:yjc_id>/', CustomNewShowView.as_view(), name='show'),
    path('list/', CustomNewListView.as_view(), name='list'),

]