"""enterprise_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls




schema_view = get_schema_view(
   openapi.Info(
      title="Funku API",
      default_version='v1',
      description="Funku description",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="rajugupta5jan1989@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('openapi', get_schema_view(
    #     title="Your Project",
    #     description="API for all things …",
    #     authentication_classes=[],
    #     permission_classes=[],
    #     version="1.0.0"
    # ), name='openapi-schema'),
    # path('', lambda request: redirect('docs/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/master/', include('master.urls')),
    path('api/property/', include('property.urls')),
    path('api/artist/', include('artist.urls')),
    path('api/promoter/', include('promoter.urls')),
    
]
