from django.urls import path
from .views import CustomNewListView, CustomNewShowView, CustomNewCategoriesNumberView

urlpatterns = [
    path('show/<int:yjc_id>/', CustomNewShowView.as_view(), name='show'),
    path('list/', CustomNewListView.as_view(), name='list'),
    path('categories-number/', CustomNewCategoriesNumberView.as_view(), name='categories-number'),
]