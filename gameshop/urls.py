
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
 
from django.views.generic import TemplateView
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/shop/',include('shop.urls')),
    path('api/personal/',include('personal.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            template_name='swagger-ui.html', url_name='schema', permission_classes=(permissions.AllowAny,),
        ),
        name='swagger-ui',
    ),

]
