from django.urls import path
from rest_framework.routers import DefaultRouter  # ViewSet'ler icin otomatik CRUD URL'leri uretir.
from . import views

# api/urls.py: app-level endpoint tanimlari.
# Neden: view'leri URL pattern'leri ile eslemek.

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),  # /products/ -> list + create
    path('products/info', views.ProductInfoAPIView.as_view()),  # /products/info -> ozet bilgi
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),  # /products/1/ -> retrieve/update/delete
]

router = DefaultRouter()  # ViewSet icin otomatik route olusturur (list, create, retrieve, update, destroy).
router.register('orders', views.OrderViewSet)  # /orders/ ve /orders/{id}/ endpoint'lerini ekler.
urlpatterns += router.urls  # Router'in urettigi URL'leri ana listeye baglar.
