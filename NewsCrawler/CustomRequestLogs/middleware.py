from .models import CustomRequestLog

class CustomRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        requested_url = request.path
        status = response.status_code
        successful = status < 400
        CustomRequestLog.objects.create(requested_url=str(requested_url), status=str(status), successful=successful)
        return response
