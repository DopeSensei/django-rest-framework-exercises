import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], #icontains instead of contains provides case sensitive
            'price': ['exact', 'lt', 'gt', 'range'] #(lt=less than, gt=grater than)
        }
#URL bar lookups;
# products/?price__lt=100
# products/?price__gt=100
# products/?price__range=100,350
# products/?name__contains=lev (for Television)
# products/?name__iexact=digital camera