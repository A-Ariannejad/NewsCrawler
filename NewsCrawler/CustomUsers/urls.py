from django.urls import path, include
from rest_framework import routers
from .views import LoginView, MyCustomUserShowView, CustomUserCreate, CustomUserDeleteView


urlpatterns = [
    path('myshow/', MyCustomUserShowView.as_view(), name='myshow'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CustomUserCreate.as_view(), name='create'),
    path('delete/<int:pk>/', CustomUserDeleteView.as_view(), name='delete'),
    
]