from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils import timezone
from .serializers import CustomUser, CustomUserLoginSerializer, GetCustomUserProfileSerializer, CustomUserSerializer
from .permissions import IsAdminUser

class CustomUserSignup(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CustomUserSerializer

class MyCustomUserShowView(generics.RetrieveAPIView):
    serializer_class = GetCustomUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            user = CustomUser.objects.get(id=user_id)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        try:
            application, created = Application.objects.get_or_create(
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_PASSWORD,
                defaults={'name': 'Default App'}
            )
        except Application.DoesNotExist:
            return Response({'error': 'No application found or created.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            expires=timezone.now() + timezone.timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            token=generate_token(),
            scope='read write'
        )
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=generate_token(),
            access_token=access_token
        )
        data = {
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'refresh_token': refresh_token.token,
            'user_id': user.id,
            'username': user.username,
        }
        return Response(data, status=status.HTTP_200_OK)
