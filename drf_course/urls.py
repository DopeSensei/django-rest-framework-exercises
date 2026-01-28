from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # API'nin tüm yapısını (endpoint'ler, request/response'lar) makine-okur formatta üretir.
    # Swagger ve Redoc gibi arayüzler bu schemayı buradan okur.

    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # API'yi tarayıcıdan görsel ve interaktif şekilde incelemek ve test etmek için kullanılır.
    # "Try it out" ile direkt request atabilirsin.

    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # API'nin daha sade, okunabilir ve paylaşmaya uygun dokümantasyon görünümüdür.
    # Genelde diğer geliştiriciler veya client'larla paylaşmak için kullanılır.

]