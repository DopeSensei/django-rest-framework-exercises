from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


###################
#@api_view(['GET'])
#def product_list(request):
#    products = Product.objects.all()
#    serializer = ProductSerializer(products, many=True)
#    return Response(serializer.data)
#    # or return JsonResponse({
#            #'data': serializer.data
#            #})

#Handles both GET and POST requests
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk') #or .exclude(stock__gt=0)  #product variable in product_detail() / .all() yerine filter()/exclude()/order_by('pk')(pagination icin) kullanabilirsin.
    #stock__gt=0 degeri 0'dan buyuk olan productlari dondurur. / exclude() sadece 0 olani dondurur.
    serializer_class = ProductSerializer  #serializer variable in product_detail()
    #filterset_fields = ('name', 'price') #Filtering (products/?name=Television)
    #filterset_fields yerine class kullanabiliiriz (filters.py)
    filterset_class = ProductFilter #(filters.py)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend] #from django_filters.rest_framework imported
    #SearchFilter = arama, #OrderingFilter = siralama
    search_fields = ['=name', 'description'] #models.py Product / "=name" for exact match
    #/products/?ordering=price
    ordering_fields = ['name', 'price', 'stock']
    #/products/?search=vision
    pagination_class = LimitOffsetPagination #PageNumberPagination
    #pagination_class.page_size = 2 #override settings.py
    #pagination_class.page_query_param = 'pagenum' #for the url bar ?pagenum=2
    #pagination_class.page_size_query_param = 'size' #costumization over how many produts we get per page
    #pagination_class.max_page_size = 6 #limit the products per page
    LimitOffsetPagination

    #Only admin can send the 'POST' request
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

#class ProductCreateAPIView(generics.CreateAPIView):
#    model = Product
#    serializer_class = ProductSerializer
#
#    def create(self, request, *args, **kwargs):
#        print(request.data)
#        return super().create(request, *args, **kwargs)


###################
#@api_view(['GET'])
#def product_detail(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    serializer = ProductSerializer(product)
#    return Response(serializer.data)

#RetrieveApiView ID'si (veya başka bir lookup alanı) verilen TEK kaydi dondurur.
#class ProductDetailAPIView(generics.RetrieveAPIView):
#    queryset = Product.objects.all()  #product variable in product_detail()
#    serializer_class = ProductSerializer  #serializer variable in product_detail()
#    lookup_url_kwarg = 'product_id'  #bunu ekleyeceksen urls.py'da 'pk'i de degistir.

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


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

##################
#@api_view(['GET'])
#def product_info(request):
#    products = Product.objects.all()
#    serializer = ProductInfoSerializer({
#        'products': products,
#        'count': len(products),
#        'max_price': products.aggregate(max_price=Max('price'))['max_price']
#    })
#    return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
            })
        return Response(serializer.data)