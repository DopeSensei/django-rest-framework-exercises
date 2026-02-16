from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache

# signals.py: model degisince cache temizlemek icin kullanilan signal handler.
# Neden: product listesi cache'leniyorsa, urun degisince eski (stale) veri kalmasin.
@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate product list caches when a product is created, updated, deleted.
    """
    print("Clearing product cahce")

    cache.delete_pattern('*product_list*') # Clear product list caches
