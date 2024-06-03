from django.urls import path, include
from rest_framework import routers
from .views import LoginView, MyCustomUserShowView, CustomUserSignup


urlpatterns = [
    path('myshow/', MyCustomUserShowView.as_view(), name='myshow'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CustomUserSignup.as_view(), name='create'),
]