from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


###################
#@api_view(['GET'])
#def product_list(request):
#    products = Product.objects.all()
#    serializer = ProductSerializer(products, many=True)
#    return Response(serializer.data)
#    # or return JsonResponse({
#            #'data': serializer.data
#            #})

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)  #product variable in product_detail() / .all() yerine filter() kullanabilirsin.
    #stock__gt=0 degeri 0'dan buyuk olan productlari dondurur. / exclude() sadece 0 olani dondurur.
    serializer_class = ProductSerializer  #serializer variable in product_detail()


###################
#@api_view(['GET'])
#def product_detail(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    serializer = ProductSerializer(product)
#    return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  #product variable in product_detail()
    serializer_class = ProductSerializer  #serializer variable in product_detail()
    lookup_url_kwarg = 'product_id'  #bunu ekleyeceksen urls.py'da 'pk'i de degistir.


##################
#@api_view(['GET'])
#def order_list(request):
#    orders = Order.objects.prefetch_related(#'items', #'items__product' yazdigimizda related name'i silebiliriz.
#        'items__product')#.all() ayni sekilde .all() da silinebilir.
#    serializer = OrderSerializer(orders, many=True)
#    return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


#Authentication yapiyoruz, order kisiye ozel gorunsun diye
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user) #yada ustteki user variable silip direkt 'qs.filter(user=self.request.user)'


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)