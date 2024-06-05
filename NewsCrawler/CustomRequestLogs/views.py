from rest_framework import generics, status
from .serializers import CustomRequestLog, GetCustomRequestLogSerializer
from django.db.models import Q
from CustomUsers.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework 
from datetime import datetime
from CustomNews.views import CustomNewPagination
from rest_framework import filters

class CustomRequestLogFilter(rest_framework.FilterSet):
    create_date = rest_framework.DateTimeFromToRangeFilter()
    class Meta:
        model = CustomRequestLog
        fields = '__all__'

class CustomRequestLogListView(generics.ListAPIView):
    queryset = CustomRequestLog.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = GetCustomRequestLogSerializer
    pagination_class = CustomNewPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CustomRequestLogFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']

class CustomRequestLogFilter(rest_framework.FilterSet):
    create_date = rest_framework.DateTimeFromToRangeFilter()
    class Meta:
        model = CustomRequestLog
        fields = ['create_date']

class CustomRequestLogNumberView(generics.ListAPIView):
    serializer_class = GetCustomRequestLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomRequestLogFilter

    def get_queryset(self):
        start_date_str = self.request.GET.get('create_date_after', None)
        end_date_str = self.request.GET.get('create_date_before', None)
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            start_date = '1800-01-01T00:00:00Z'
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            end_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        queryset = CustomRequestLog.objects.filter(create_date__range=[start_date, end_date]).all()
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        successful_count = queryset.filter(successful=True).count()
        res={
            'all': count,
            'successful': successful_count,
            'unsuccessful': count - successful_count,
        }
        return Response(res, status=status.HTTP_200_OK)
