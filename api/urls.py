from django.urls import path
from . import views

# api/urls.py: app-level endpoint tanimlari.
# Her path ilgili view class'ini cagirir.

urlpatterns = [
    # /products/ -> listele + yeni product olustur
    path('products/', views.ProductListCreateAPIView.as_view()),
    # /products/info -> extra bilgi (count, max_price)
    path('products/info', views.ProductInfoAPIView.as_view()),
    # /products/<product_id>/ -> tek product getir/guncelle/sil
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    # /orders/ -> tum order'lari listeler
    path('orders/', views.OrderListAPIView.as_view()),
    # /user-orders/ -> sadece login kullanicinin order'lari
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders')
]
