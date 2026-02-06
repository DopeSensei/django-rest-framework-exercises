from django.db.models import Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer)

# views.py: API endpoint davranislarini topladigimiz katman.
# Neden: HTTP istegini queryset + serializer + permission ile birlestirip response uretiriz.

# 1.1.
"""
# Function-based view ornegi: sadece GET ile product listesi doner.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()  # ORM ile tum Product kayitlarini getirir.
    serializer = ProductSerializer(products, many=True)  # QuerySet -> JSON listesi formatina cevirir.
    return Response(serializer.data)
    # or return JsonResponse({
            #'data': serializer.data
            #})
"""

# 1.2
"""
# Generic CreateAPIView ornegi: sadece POST ile product olusturur.
class ProductCreateAPIView(generics.CreateAPIView):
    model = Product  # Bu view'in uzerinden create edilecek model sinifi.
    serializer_class = ProductSerializer  # Request body validation + DB create icin serializer.

    # create override: request.data'yi gormek/ozellestirmek icin.
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
"""

# 1.3.
# Product listesi + yeni product olusturma endpoint'i (GET/POST).
# Neden: listeleme ve create icin ayri endpoint yazmadan DRF generic kullanmak.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')  # Base QuerySet; pagination stabil olsun diye pk ile siralar.
    serializer_class = ProductSerializer  # Response ve POST/PUT body formatini belirler.
    #filterset_fields = ('name', 'price') # Filtering (products/?name=Television)
    #filterset_fields yerine class kullanabiliiriz (filters.py)
    filterset_class = ProductFilter  # django-filter ile alan bazli filtreleri buradan alir.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]  # Query param ile filtre/arama/siralama + custom stok filtresi.
    search_fields = ['=name', 'description']  # SearchFilter bunlari kullanir; '=name' exact match, description partial.
    ordering_fields = ['name', 'price', 'stock']  # OrderingFilter icin whitelist; ?ordering=price gibi.
    pagination_class = LimitOffsetPagination  # ?limit=..&offset=.. seklinde pagination kullan.
    #pagination_class.page_size = 2 #override settings.py
    #pagination_class.page_query_param = 'pagenum' #for the url bar ?pagenum=2
    #pagination_class.page_size_query_param = 'size' #costumization over how many produts we get per page
    #pagination_class.max_page_size = 6 #limit the products per page
    LimitOffsetPagination  # Tek basina yazilinca etkisi yok; sadece not olarak kalmis.

    # GET herkese acik, POST icin admin kontrolu uygular.
    def get_permissions(self):
        self.permission_classes = [AllowAny]  # Varsayilan: okuma istekleri serbest.
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]  # Create sadece admin; veri kontrolu icin.
        return super().get_permissions()  # DRF permission instance'larini olusturur.

##########################################################################

# 2.1.
"""
# Function-based view ornegi: tek product GET ile dondurur.
@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Id bulunamazsa otomatik 404 d?ner.
    serializer = ProductSerializer(product)  # Tek obje serialize edilir.
    return Response(serializer.data)
"""

# 2.2.
"""
# RetrieveAPIView ornegi: tek kayit sadece GET ile dondurulur.
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # Tekil kaydi bulmak icin base QuerySet.
    serializer_class = ProductSerializer  # Read icin serializer.
    lookup_url_kwarg = 'product_id'  # URL'de pk yerine bu parametre kullanilir.
"""

# 2.3.
# Tek product kaydini getirir; PUT/PATCH/DELETE ile guncelleme/silme yapar.
# Neden: read + update + delete tek endpoint'te toplanir.
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()  # Detail view icin gerekli base QuerySet.
    serializer_class = ProductSerializer  # Hem read hem write icin serializer.
    lookup_url_kwarg = 'product_id'  # URL param adini 'product_id' olarak map eder.

    # PUT/PATCH/DELETE sadece admin, GET herkese acik.
    def get_permissions(self):
        self.permission_classes = [AllowAny]  # GET icin serbest.
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Yazma/silme icin admin yetkisi.
        return super().get_permissions()

##########################################################################

# 3.1.
"""
# Function-based view ornegi: tum order'lari listeler.
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items__product')  # N+1 azaltmak icin item+product prefetch.
    serializer = OrderSerializer(orders, many=True)  # QuerySet -> JSON listesi.
    return Response(serializer.data)
"""

# 3.2.
"""
# Tum order'lari listeler. Neden: admin raporlama veya genel listeleme.
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')  # OrderItem + Product verisini tek seferde ceker.
    serializer_class = OrderSerializer  # Order + nested item bilgilerini doner.

# Sadece giris yapan kullanicinin order'larini listeler.
# Neden: kullanici gizliligi (herkes herkesi gormesin).
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')  # Related veriyi performans icin prefetch eder.
    serializer_class = OrderSerializer  # Response formatini belirler.
    permission_classes = [IsAuthenticated]  # Login zorunlu; request.user set edilsin.

    # request.user'a gore filtrelenmis QuerySet dondurur.
    def get_queryset(self):
        user = self.request.user  # Auth middleware + DRF auth ile gelen user.
        qs = super().get_queryset()  # Base QuerySet (Order.objects...).
        return qs.filter(user=user)  # Yalnizca bu user'in siparisleri.
"""

# 3.3.
# Order icin tam CRUD saglayan ViewSet.
# Neden: router ile otomatik list/create/retrieve/update/delete endpoint'leri olusur.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')  # Nested serializer icin prefetch; sorgu sayisini azaltir.
    serializer_class = OrderSerializer  # Order + items formatini belirler.
    permission_classes = [IsAuthenticated]  # Tumu icin login zorunlu; guest erisimi kapatir.
    pagination_class = None  # ViewSet'te pagination istemiyorsan None (tum listeyi tek response).
    filterset_class = OrderFilter  # /orders/?status=Pending gibi filtreleri aktif eder.
    filter_backends = [DjangoFilterBackend]  # filterset_class'in calismasi icin backend gerekir.

    # Staff ise tum order'lari gor, degilse sadece kendi order'larini goster.
    # Neden: normal user baska kullanicinin verisini gormesin.
    def get_queryset(self):
        qs = super().get_queryset()  # ViewSet'in base queryset'ini al.
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)  # Normal user icin sadece kendi order'lari.
        return qs  # Staff ise filtre uygulanmadan doner.

##########################################################################

# 4.1.
"""
# Function-based view ornegi: count ve max_price gibi ozet bilgiler dondurur.
@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()  # Butun product'lar.
    serializer = ProductInfoSerializer({
        'products': products,  # QuerySet.
        'count': len(products),  # Toplam adet.
        'max_price': products.aggregate(max_price=Max('price'))['max_price']  # En yuksek fiyat.
    })
    return Response(serializer.data)
"""

# 4.2.
# Custom response icin APIView kullaniyoruz (standart generics degil).
# Neden: list + aggregate (count, max_price) ayni response'ta donsun.
class ProductInfoAPIView(APIView):
    # GET: product listesi + count + max_price doner.
    def get(self, request):
        products = Product.objects.all()  # QuerySet.
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
            })  # Dict -> serializer ile tek response.
        return Response(serializer.data)
