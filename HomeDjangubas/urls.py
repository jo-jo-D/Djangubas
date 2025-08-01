"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from shop.views import LoginView

schema_view = get_schema_view(
       openapi.Info(
              title="Djangubas Project API",
              default_version='v1',
              description="API documentation for my first project.",
              terms_of_service="https://www.google.com/policies/terms/",
              contact=openapi.Contact(email="contact@myproject.local"),
              license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
       path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
       path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
       path('admin/', admin.site.urls),
       path('app1/', include('app1.urls')),
       #path('', include('library.urls')), # http://127.0.0.1:8000/project/my_path
       path('project/', include('project.urls')), ## http://127.0.0.1:8000/project/admin/
       path('', include('task_manager.urls')), ## http://127.0.0.1:8000/project/admin/
       path('library/', include('library.urls')),
       path('shop/', include('shop.urls')),
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       path('get-token/', obtain_auth_token, name='get token'),
]

