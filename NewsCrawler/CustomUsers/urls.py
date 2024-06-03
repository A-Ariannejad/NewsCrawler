from django.urls import path, include
from rest_framework import routers
from .views import LoginView, MyCustomUserShowView, CustomUserCreateView, CustomUserDeleteView, CustomUserUpdateView, CustomUserShowView, CustomUserListView


urlpatterns = [
    path('myshow/', MyCustomUserShowView.as_view(), name='myshow'),
    path('show/<int:id>/', CustomUserShowView.as_view(), name='show'),
    path('list/', CustomUserListView.as_view({'get': 'list'}), name='list'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CustomUserCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', CustomUserDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', CustomUserUpdateView.as_view(), name='update'),

]