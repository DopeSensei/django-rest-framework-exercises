from django.contrib import admin
from api.models import Order, OrderItem, User

# admin.py: Django admin paneli konfigurasyonu.
# Neden: admin arayuzunde Order + OrderItem'lari rahat gormek.

# Order icinde OrderItem'lari tablo halinde gosterir (inline).
class OrderItemInline(admin.TabularInline):
    model = OrderItem  # Inline olarak gosterilecek model.

# Order admin: inline olarak order item'lari gormek icin.
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order, OrderAdmin)  # Order icin ozellestirilmis admin.
admin.site.register(User)  # User modelini admin'e ekler.
