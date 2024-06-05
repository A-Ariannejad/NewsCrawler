from rest_framework import status, generics, permissions
from .serializers import CustomNew, GetCustomNewSerializer
from rest_framework.pagination import PageNumberPagination
from .serializers import GetCustomNewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework 
from rest_framework import filters
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q

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

class CustomNewCategoriesNumberView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetCustomNewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomNewCategoriesNumberFilter
    
    def get_queryset(self):
        start_date_str = self.request.GET.get('pubDate_ad_after', None)
        end_date_str = self.request.GET.get('pubDate_ad_before', None)
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%SZ')
        else:
            start_date = '1800-01-01T00:00:00Z'
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%SZ')
        else:
            end_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        queryset = CustomNew.objects.filter(create_date__range=[start_date, end_date]).all()
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        res ={
        'all_news': queryset.filter(Q(category='all_news') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'first_page': queryset.filter(Q(category='first_page') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'election': queryset.filter(Q(category='election') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'international': queryset.filter(Q(category='international') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'sports': queryset.filter(Q(category='sports') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'social': queryset.filter(Q(category='social') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'economics': queryset.filter(Q(category='economics') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'arts': queryset.filter(Q(category='arts') & (Q(status='latest') | Q(status='most_visited'))).count(),
        'medical': queryset.filter(Q(category='medical') & (Q(status='latest') | Q(status='most_visited'))).count(),
        }
        return Response(res, status=status.HTTP_200_OK)





