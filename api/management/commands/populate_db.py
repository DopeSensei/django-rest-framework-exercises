import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem

# populate_db: ornek veri ureten management command.
# Neden: gelistirme/test icin hizli dummy data uretmek.
# Calistirma: python manage.py populate_db

class Command(BaseCommand):
    help = 'Creates application data'  # manage.py help listesinde gorunen aciklama.

    # handle: komut calistiginda tetiklenen ana fonksiyon.
    def handle(self, *args, **kwargs):
        user = User.objects.filter(username='admin').first()  # Admin user varsa al.
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')  # Yoksa olustur.

        products = [
            Product(name="A Scanner Darkly", description=lorem_ipsum.paragraph(), price=Decimal('12.99'), stock=4),
            Product(name="Coffee Machine", description=lorem_ipsum.paragraph(), price=Decimal('70.99'), stock=6),
            Product(name="Velvet Underground & Nico", description=lorem_ipsum.paragraph(), price=Decimal('15.99'), stock=11),
            Product(name="Enter the Wu-Tang (36 Chambers)", description=lorem_ipsum.paragraph(), price=Decimal('17.99'), stock=2),
            Product(name="Digital Camera", description=lorem_ipsum.paragraph(), price=Decimal('350.99'), stock=4),
            Product(name="Watch", description=lorem_ipsum.paragraph(), price=Decimal('500.05'), stock=0),
        ]  # Ornek product listesi (name, desc, price, stock).

        Product.objects.bulk_create(products)  # Toplu ekleme (performansli).
        products = Product.objects.all()  # DB'den tekrar cek.

        for _ in range(3):  # 3 adet ornek order olustur.
            order = Order.objects.create(user=user)  # Order admin user'a ait.
            for product in random.sample(list(products), 2):  # Her order'a 2 urun ekle.
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1,3)
                )
