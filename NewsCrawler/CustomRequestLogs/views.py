from django.db.models.functions import TruncMinute
from django.db.models import Count
from rest_framework import generics
from .models import CustomRequestLog
from .serializers import GetCustomRequestLogSerializer
from django.db.models import Q

class RequestLogView(generics.ListAPIView):
    serializer_class = GetCustomRequestLogSerializer

    def get_queryset(self):
        return CustomRequestLog.objects.annotate(
            minute=TruncMinute('create_date')
        ).values('minute').annotate(
            total_requests=Count('id'),
            successful_requests=Count('id', filter=Q(status=True)),
            unsuccessful_requests=Count('id', filter=Q(status=False)),
        ).order_by('minute')
