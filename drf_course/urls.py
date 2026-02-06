from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# drf_course/urls.py: proje seviyesindeki URL konfigurasyonu.
# Burada app URL'lerini ve global endpoint'leri bagliyoruz.

urlpatterns = [
    # Django admin paneli
    path('admin/', admin.site.urls),
    # api app URL'leri
    path('', include('api.urls')),
    # Silk profiling arayuzu
    path('silk/', include('silk.urls', namespace='silk')),

    # JWT token alma ve yenileme
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # API'nin tum yapisini (endpoint'ler, request/response) makine-okur formatta uretir.
    # Swagger ve Redoc gibi arayuzler bu schemayi buradan okur.

    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # API'yi tarayicidan gorsel ve interaktif sekilde incelemek ve test etmek icin kullanilir.
    # "Try it out" ile direkt request atabilirsin.

    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # API'nin daha sade, okunabilir ve paylasmaya uygun dokumantasyon gorunumudur.
    # Genelde diger gelistiriciler veya client'larla paylasmak icin kullanilir.

]
