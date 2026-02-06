from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status

# tests.py: basit endpoint testleri.
# Neden: yetki ve filtreleme davranislarini otomatik dogrulamak.

# UserOrderList endpoint'i sadece login kullanicinin order'larini getirmeli.
class UserOrderTestCase(TestCase):
    # setUp: her testten once calisir; test verisi olusturur.
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')  # Ornek user.
        user2 = User.objects.create_user(username='user2', password='test')  # Ornek user.
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    # Auth olan user sadece kendi order'larini gormeli.
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user2')
        self.client.force_login(user)  # Test client ile login yap.
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders))

    # Login olmayan istek 401 donmeli.
    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
