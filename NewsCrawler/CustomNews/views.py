from rest_framework import status, generics, viewsets, permissions
from .serializers import CustomNew, GetCustomNewSerializer
from CustomUsers.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .serializers import GetCustomNewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework 
from rest_framework import filters
from rest_framework.response import Response
from datetime import datetime

class CustomNewFilter(rest_framework.FilterSet):
    pubDate_ad = rest_framework.DateTimeFromToRangeFilter()
    class Meta:
        model = CustomNew
        fields = ['category', 'status', 'pubDate_ad']

class CustomNewCategoriesNumberFilter(rest_framework.FilterSet):
    pubDate_ad = rest_framework.DateTimeFromToRangeFilter()
    class Meta:
        model = CustomNew
        fields = ['pubDate_ad']

class CustomNewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomNewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomNewListView(generics.ListAPIView):
    queryset = CustomNew.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetCustomNewSerializer
    pagination_class = CustomNewPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomNewFilter
    search_fields = ['category', 'title', 'link', 'yjc_id', 'description']
    ordering_fields = ['create_date']
    ordering = ['-create_date']

class CustomNewShowView(generics.RetrieveAPIView):
    queryset = CustomNew.objects.all()
    serializer_class = GetCustomNewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'yjc_id'







