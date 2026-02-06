from rest_framework import serializers
from .models import Product, Order, OrderItem

# serializers.py: API payload'larini Python objelerine cevirir ve validation yapar.
# Neden: request/response formatini tek yerde kontrol etmek.


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


# Order serializer: order + nested items + hesaplanan toplam fiyat.
class OrderSerializer(serializers.ModelSerializer):
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
