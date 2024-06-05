from .models import RequestLog

class CustomRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        status = response.status_code
        successful = response.status_code < 400
        RequestLog.objects.create(status=status, successful=successful)
        return response