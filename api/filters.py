import django_filters
from api.models import Product
from rest_framework import filters

# filters.py: django-filters ve custom filter backend'ler bu dosyada.

# Custom filter backend: stokta olan urunleri (stock > 0) getirir.
# Bu backend eklendiginde her request'te otomatik uygulanir; ekstra query param gerekmez.
class InStockFilterBackend(filters.BaseFilterBackend):
    # filter_queryset: DRF filter backend contract'i.
    # request ve view bilgisi gelir; queryset return edilince response bu sekilde filtrelenir.
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


# DjangoFilterBackend icin filtre seti: URL query paramlari ile alan bazli filtreleme.
class ProductFilter(django_filters.FilterSet):
    class Meta:
        # model: hangi model icin filter tanimladigimizi belirtir.
        model = Product
        # fields: her alan icin izin verilen lookup'lar.
        fields = {
            'name': ['iexact', 'icontains'], # icontains case-insensitive arama yapar.
            'price': ['exact', 'lt', 'gt', 'range'] #(lt=less than, gt=greater than)
        }
# URL bar lookups:
# products/?price__lt=100
# products/?price__gt=100
# products/?price__range=100,350
# products/?name__icontains=lev (for Television)
# products/?name__iexact=digital camera
