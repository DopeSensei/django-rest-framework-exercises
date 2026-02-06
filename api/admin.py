from django.contrib import admin
from api.models import Order, OrderItem, User

# admin.py: Django admin paneli konfigurasyonu.

# Order icinde OrderItem'lari tablo halinde gosterir (inline).
class OrderItemInline(admin.TabularInline):
    model = OrderItem

# Order admin: inline olarak order item'lari gormek icin.
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

# Model kayitlari
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
