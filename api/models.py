import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# models.py: veritabani tablolarini ve iliskileri tanimlar.

# Custom User modeli: ileride ekstra alan eklemek icin AbstractUser'dan turetilir.
# settings.py icindeki AUTH_USER_MODEL ile bu model kullanilir.
class User(AbstractUser):
    pass


class Product(models.Model):
    # name: urun adi.
    name = models.CharField(max_length=200)
    # description: uzun aciklama.
    description = models.TextField()
    # price: para alani; max_digits toplam basamak, decimal_places ondalik basamak.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock: negatif olmayacak sayi.
    stock = models.PositiveIntegerField()
    # image: urun resmi; MEDIA_ROOT/products/ altina kaydeder. Bos birakilabilir.
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # in_stock: DB'de alan degil, hesaplanan property.
    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        # __str__: Django admin/console'da okunabilir isim.
        return self.name


class Order(models.Model):
    # StatusChoices: order durumlari icin sabit liste.
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    # order_id: UUID primary key, otomatik olusturulur (auto-increment yok).
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # user: siparisi veren kullanici; user silinirse siparisler de silinir.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_at: kayit olusunca otomatik zaman.
    created_at = models.DateTimeField(auto_now_add=True)
    # status: StatusChoices ile sinirli deger.
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    # products: ManyToMany, ama ara tablo OrderItem (quantity gibi ekstra alan icin).
    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')

    def __str__(self):
        # __str__: admin/console icin okunabilir metin.
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    # order: ilgili siparis; related_name='items' -> order.items ile erisim.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # product: ilgili urun.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # quantity: siparisteki adet.
    quantity = models.PositiveIntegerField()

    # item_subtotal: urun fiyati * adet; DB'de tutulmaz.
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        # __str__: admin/console icin okunabilir metin.
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
