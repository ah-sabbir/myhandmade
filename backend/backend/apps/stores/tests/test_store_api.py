from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from backend.apps.users.models import User
from .models import Store

class StoreCreationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="storeowner", password="storepass123")
        self.client.force_authenticate(user=self.user)

    def test_store_creation(self):
        url = reverse('store-create')
        data = {"name": "Test Store", "description": "Store for testing"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class StoreDetailsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="storeowner", password="storepass123")
        self.store = Store.objects.create(owner=self.user, name="Test Store")
        self.client.force_authenticate(user=self.user)

    def test_store_retrieve(self):
        url = reverse('store-detail', args=[self.store.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Store")
