from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# drf_course/urls.py: proje seviyesindeki URL konfigurasyonu.
# Neden: app URL'lerini ve global endpoint'leri tek merkezde toplamak.

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneli
    path('', include('api.urls')),  # api app URL'leri
    path('silk/', include('silk.urls', namespace='silk')),  # Silk profiling arayuzu

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT access+refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI schema (makine-okur)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc UI
]
