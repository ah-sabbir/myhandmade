# store/tests/test_products_api.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from backend.apps.products.models import Product
from django.contrib.auth.models import User

class ProductAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication purposes
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Log the user in
        self.client.login(username="testuser", password="testpassword")
        
        # Create sample products
        self.product1 = Product.objects.create(name="Sample Product 1", price=100.0, stock=10)
        self.product2 = Product.objects.create(name="Sample Product 2", price=150.0, stock=5)
        
        # URL patterns for the test cases
        self.list_url = reverse("product-list")
        self.detail_url = lambda pk: reverse("product-detail", args=[pk])

    def test_get_product_list(self):
        # Test retrieving the product list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Checking if the two products created in setup are returned

    def test_create_product(self):
        # Test creating a new product
        data = {
            "name": "New Product",
            "price": 200.0,
            "stock": 20
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)  # Confirming a new product was added

    def test_get_product_detail(self):
        # Test retrieving a specific product
        response = self.client.get(self.detail_url(self.product1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product1.name)

    def test_update_product(self):
        # Test updating a product
        data = {
            "name": "Updated Product Name",
            "price": 120.0,
            "stock": 15
        }
        response = self.client.put(self.detail_url(self.product1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()  # Refresh from database to get the latest data
        self.assertEqual(self.product1.name, "Updated Product Name")

    def test_delete_product(self):
        # Test deleting a product
        response = self.client.delete(self.detail_url(self.product1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)  # Confirming one product was deleted
