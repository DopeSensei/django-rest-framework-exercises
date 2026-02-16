from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem, User

# serializers.py: API payload'larini Python objelerine cevirir ve validation yapar.
# Neden: request/response formatini tek yerde kontrol etmek.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # exclude = ('password', 'user_permissions', 'get_full_name') # Istemedigin fieldlari cikarir geri kalan hepsini yazdirir. exclude() 'is_authenticated' dondurmez.
            #'__all__' # Best practice degil!
            'username',
            'password',
            'email',
            'is_staff',
            'is_superuser',
            'get_full_name',
            'user_permissions',
            'orders' #models.py/Order class/user variable/related_name='orders'. / Related name atamadiysan bu field'i 'order_set' olarak yazmalisin.
        )

# Product modeli icin serializer (read/write).
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Hangi modelin alanlari kullanilacak.
        fields = (  # API'de gosterilecek alanlar; ID DB'de uretildigi icin eklenmedi.
            'description',
            'name',
            'price',
            'stock',
        )

    # price alanini dogrular; negatif/0 fiyatlari engeller.
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value


# OrderItem serializer: order icindeki her satiri (urun+adet) temsil eder.
class OrderItemSerializer(serializers.ModelSerializer):
    # source=... ile Product uzerinden alan cekiyoruz; nested serializer yazmadan hafif cozum.
    # Neden: sadece gereken alanlari gostermek ve response'u kucuk tutmak.
    product_name = serializers.CharField(source='product.name')  # OrderItem -> Product.name degerini response'a yazar.
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price')  # OrderItem -> Product.price degerini response'a yazar.
    class Meta:
        model = OrderItem  # Hangi modelin alanlari alinacak.
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )


# OrderCreateSerializer: write (create/update) islemleri icin kullanilir.
# Neden: nested items (OrderItem) create/update varsayilan ModelSerializer ile otomatik yapilmaz.
class OrderCreateSerializer(serializers.ModelSerializer):
    # OrderItemCreateSerializer: request icindeki items listesi icin nested write serializer.
    # Neden: sadece product ve quantity alanlarini alarak daha sade bir input beklemek.
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')  # product FK id + quantity; price gibi alanlar product'tan gelir.

    order_id = serializers.UUIDField(read_only=True)  # Order id'yi response'ta gormek icin; request'te gonderilmez.
    items = OrderItemCreateSerializer(many=True, required=False)  # many=True -> liste; required=False -> items gelmezse validation fail olmasin (PATCH icin).

    # update override: nested OrderItem'lari manuel guncellemek icin.
    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')  # items verisini ayir; Order modelinde alan degil.

        with transaction.atomic():  # Tum islemler tek transaction; hata olursa hepsi rollback.
            instance = super().update(instance, validated_data)  # Order modelinin normal alanlarini update eder.

            if orderitem_data is not None:
                instance.items.all().delete()  # Var olan itemleri silip yenilerini yaziyoruz (replace mantigi).

                # Update edilmis data ile itemlari tekrar olustur.
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)  # item dict -> product, quantity.

        return instance

    # create override: Order + OrderItem'lari ayni request'te olusturmak icin.
    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')  # items listesi Order tablosuna yazilmayacak.

        # transaction.atomic: bu block icindeki DB islemleri ya tamamen basarili olur ya da geri alinir.
        with transaction.atomic():
            order = Order.objects.create(**validated_data)  # Order kaydini olustur (user, status gibi alanlar).

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)  # Her item icin OrderItem olustur.

        return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items'
        )
        extra_kwargs = {
            'user': {'read_only': True} # 'user'i POST requestlerde otomatik olarak ayarlar.
        }


# Order serializer: order + nested items + hesaplanan toplam fiyat.
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)  # related_name='items' uzerinden nested serializer.
    total_price = serializers.SerializerMethodField(method_name='total')  # DB'de olmayan hesaplanan alan.

    # total_price icin hesaplama fonksiyonu; neden: toplam fiyat DB'de tutulmaz.
    def total(self, obj):
        order_items = obj.items.all()  # OrderItem listesi (related_name='items').
        return sum(order_item.item_subtotal for order_item in order_items)  # Her satirin subtotal'ini toplar.

    class Meta:
        model = Order  # Hangi model.
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price'
        )


# Custom/standart olmayan response icin plain Serializer.
class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)  # QuerySet'i nested list olarak doner.
    count = serializers.IntegerField()  # Toplam adet.
    max_price = serializers.FloatField()  # En yuksek fiyat.


# =====================================================
# Serializer vs ModelSerializer (Ozet Tablo)
# =====================================================

# Ozellik            | Serializer                  | ModelSerializer
# ------------------ | --------------------------- | ------------------------------
# Modele bagli mi?   | Hayir                       | Evet
# Field tanimi       | Manuel                      | Otomatik (modelden)
# CRUD uyumu         | Zayif                       | Guclu
# create / update    | Manuel                      | Otomatik
# Validation         | Manuel                      | Otomatik
# Model disi veri    | Evet                        | Hayir
# Esneklik           | Yuksek                      | Orta
# Kod miktari        | Fazla                       | Az
# Bakim kolayligi    | Dusuk                       | Yuksek
# Kullanim alani     | Ozet / Istatistik / Custom  | Standart REST API
# =====================================================
