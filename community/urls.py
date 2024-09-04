from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib import admin
from django.urls import path, include
from board.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Reeun APIs",
      default_version='v1',
      description="Test description",
      terms_of_service="<https://www.google.com/policies/terms/>",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('member/', include('member.urls')),
    path('classboard/', include('classboard.urls')),
    path('message/', include('message.urls')),
    path('dj/', include('dj_rest_auth.urls')),
    path('dj/registration/', include('dj_rest_auth.registration.urls')),


    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

