from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils import timezone
from .serializers import CustomUser, LoginCustomUserSerializer, GetCustomUserProfileSerializer, CreateCustomUserSerializer, UpdateCustomUserSerializer, RefreshTokenCustomUserSerializer
from .permissions import IsAdminUser
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate

class CustomUserShowView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = GetCustomUserProfileSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class CustomUserListView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GetCustomUserProfileSerializer
    permission_classes = [IsAdminUser]
    
class CustomUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateCustomUserSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(password=make_password(self.request.data.get('password')))

class CustomUserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = GetCustomUserProfileSerializer

class CustomUserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer

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
    serializer_class = LoginCustomUserSerializer

    @swagger_auto_schema(request_body=LoginCustomUserSerializer)
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
        access_token = AccessToken.objects.filter(user=user, application=application).all()
        if access_token:
            access_token.delete()
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

class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenCustomUserSerializer

    @swagger_auto_schema(request_body=RefreshTokenCustomUserSerializer)
    def post(self, request, *args, **kwargs):
        refresh_token_value = request.data.get('refresh_token')
        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_value)
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        access_token = refresh_token.access_token
        if access_token.expires < timezone.now():
            return Response({'error': 'Refresh token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        new_access_token = AccessToken.objects.create(
            user=access_token.user,
            application=access_token.application,
            expires=timezone.now() + timezone.timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            token=generate_token(),
            scope=access_token.scope,
        )
        access_token.delete()
        data = {
            'access_token': new_access_token.token,
            'token_type': 'Bearer',
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        }
        return Response(data, status=status.HTTP_200_OK)

