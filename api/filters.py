import django_filters
from api.models import Product, Order
from rest_framework import filters

# filters.py: django-filters ve custom filter backend'ler burada.
# Neden: view katmaninda query param filtreleme ve reusable filter mantigi saglamak.

# Custom filter backend: stokta olan urunleri (stock > 0) getirir.
# Neden: ekstra query param gerektirmeden otomatik stok filtresi uygulamak.
class InStockFilterBackend(filters.BaseFilterBackend):
    # filter_queryset: DRF filter backend contract'i.
    # request -> query paramlar ve user bilgisi; view -> hangi view oldugu.
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)  # Stokta olanlari dondurur (stock > 0).


# Product icin query param filtreleri (django-filter).
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product  # Bu filter hangi modele ait.
        fields = {
            'name': ['iexact', 'icontains'], # name__iexact=... veya name__icontains=... kullanabilirsin.
            'price': ['exact', 'lt', 'gt', 'range'] # price__lt=, price__gt=, price__range=100,200
        }
# URL bar lookups:
# products/?price__lt=100
# products/?price__gt=100
# products/?price__range=100,350
# products/?name__icontains=lev (for Television)
# products/?name__iexact=digital camera


# Order icin query param filtreleri (django-filter).
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')  # DateField'e cevirir; sadece tarih bazli filtre icin.
    class Meta:
        model = Order  # Bu filter hangi modele ait.
        fields = {
            'status': ['exact'],  # status=Pending gibi.
            'created_at': ['lt', 'gt', 'exact']  # created_at__lt=2026-02-01 gibi.
            }
