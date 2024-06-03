"""
URL configuration for NewsCrawler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, authentication
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

schema_view = get_schema_view(
    openapi.Info(
        title="News Crawler",
        default_version='v1',
        description="This project involves creating a backend application using Django Rest Framework that crawls a news website to extract and store essential information, which users can access. The application features two user roles—users and admins—managed through a secure OAuth 2.0 authentication system.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.TokenAuthentication,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('user/', include('CustomUsers.urls')),
]
