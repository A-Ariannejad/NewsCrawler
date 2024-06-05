from rest_framework import status, generics, viewsets, permissions
from .serializers import CustomNew, GetCustomNewSerializer
from CustomUsers.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import CustomNew
from .serializers import GetCustomNewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework 
from rest_framework import filters

class CustomNewFilter(rest_framework.FilterSet):
    pubDate_ad = rest_framework.DateTimeFromToRangeFilter()
    pubDate_solar = rest_framework.DateTimeFromToRangeFilter()
    class Meta:
        model = CustomNew
        fields = '__all__'

class CustomNewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomNewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomNewListView(ListAPIView):
    queryset = CustomNew.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GetCustomNewSerializer
    pagination_class = CustomNewPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomNewFilter
    search_fields = ['category', 'title', 'link', 'yjc_id', 'description']
    ordering_fields = ['create_date']
    ordering = ['-create_date']




