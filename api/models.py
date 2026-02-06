import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# models.py: veritabani tablolarini ve iliskileri tanimlar.
# Neden: ORM uzerinden DB schema'sini tek yerde kontrol etmek.

# Custom User modeli: ileride ekstra alan eklemek icin AbstractUser'dan turetilir.
class User(AbstractUser):
    pass  # AUTH_USER_MODEL ile bu model kullanilir (settings.py).


class Product(models.Model):
    name = models.CharField(max_length=200)  # Urun adi; max_length DB'de string limitidir.
    description = models.TextField()  # Uzun aciklama; length limiti yok.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Para icin Decimal kullanilir (float hata yapabilir).
    stock = models.PositiveIntegerField()  # Negatif olamaz; stok sayisi.
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Opsiyonel resim; MEDIA_ROOT/products/ altina kaydeder.

    # DB'de alan degil, hesaplanan property; neden: stok kontrolunu kolay okumak.
    @property
    def in_stock(self):
        return self.stock > 0

    # Admin/console'da okunabilir isim.
    def __str__(self):
        return self.name


class Order(models.Model):
    # Order durumlarini sabitlemek icin TextChoices kullanilir.
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # Auto-increment yerine UUID kullanir.
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Siparisi veren kullanici; user silinirse order'lar silinir.
    created_at = models.DateTimeField(auto_now_add=True)  # Kayit olusunca otomatik zaman.
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)  # Durum alani; choices ile sinirli.

    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')  # Quantity gibi ek alan icin ara tablo kullanilir.

    # Admin/console'da okunabilir metin.
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # order.items ile erisim; siparis silinirse item'lar silinir.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Siparisteki urun; urun silinirse item da silinir.
    quantity = models.PositiveIntegerField()  # Siparis adedi; negatif olamaz.

    # DB'de alan degil; toplam satir tutarini hesaplar.
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    # Admin/console icin okunabilir metin.
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
