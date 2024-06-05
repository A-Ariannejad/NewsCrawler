from .models import CustomRequestLog, CustomUser

class CustomRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        requested_url = request.path
        status = response.status_code
        successful = status < 400
        user = CustomUser.objects.filter(id=request.user.id).first()
        CustomRequestLog.objects.create(requested_url=str(requested_url), status=str(status), successful=successful, owner=user)
        return response
