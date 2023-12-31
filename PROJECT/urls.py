from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Quiz Test API",
      default_version='v1',
      description="Quiz Test API via Django Admin interface",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="otabecktursunov@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quizApp.urls')),

    # Swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0))
]
