from rest_framework.throttling import UserRateThrottle

# BurstRateThrottle: kisa surede hizli istekleri sinirlar (ani yuklenmeleri yakalar).
# Neden: API'nin bir anda cok fazla istek alip cökmesini onlemek; rate degeri settings.py'de belirlenir.
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'  # DEFAULT_THROTTLE_RATES icinde 'burst' key'i ile eslesir.

# SustainedRateThrottle: daha uzun vadeli genel kullanimi sinirlar (sabit hiz).
# Neden: tek kullanicinin uzun sure API'yi suistimal etmesini engellemek.
class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'  # DEFAULT_THROTTLE_RATES icinde 'sustained' key'i ile eslesir.
