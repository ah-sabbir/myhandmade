from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.registration_url = reverse('register')  # Adjust if different
        self.login_url = reverse('login')  # Adjust if different
        # self.profile_url = reverse('user-profile')  # Profile endpoint for GET and PUT

        # Valid user registration data
        self.valid_registration_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'phone_number': '+1234567890',
            'user_type': 'customer'
        }

        # Another user for login testing
        self.user_data_for_login = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'janesmith@example.com',
            'password': 'AnotherStrongPassword123!'
        }

        # Create a user manually for login tests
        self.user = User.objects.create_user(
            first_name=self.user_data_for_login['first_name'],
            last_name=self.user_data_for_login['last_name'],
            email=self.user_data_for_login['email'],
            password=self.user_data_for_login['password'],
        )

    # User Registration Tests
    def test_register_user_success(self):
        response = self.client.post(self.registration_url, self.valid_registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.valid_registration_data['email']).exists())

    def test_register_user_password_mismatch(self):
        data = self.valid_registration_data.copy()
        data['password2'] = 'DifferentPassword123!'
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_user_duplicate_email(self):
        # Register the first user
        self.client.post(self.registration_url, self.valid_registration_data)

        # Try registering with the same email again
        response = self.client.post(self.registration_url, self.valid_registration_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_user_missing_fields(self):
        response = self.client.post(self.registration_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    # User Login Tests
    def test_login_user_success(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data_for_login['email'],
            'password': self.user_data_for_login['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming token authentication is used

    def test_login_user_invalid_password(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data_for_login['email'],
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


    def test_login_user_unregistered_email(self):
        response = self.client.post(self.login_url, {
            'email': 'unregistered@example.com',
            'password': 'SomePassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    # # Profile Update Tests
    def test_update_user_profile_success(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    #     # Update the user's profile
    #     response = self.client.put(self.profile_url, {
    #         'first_name': 'UpdatedFirstName',
    #         'last_name': 'UpdatedLastName',
    #         'phone_number': '+19876543210'
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['first_name'], 'UpdatedFirstName')
    #     self.assertEqual(response.data['last_name'], 'UpdatedLastName')

    # def test_update_user_profile_unauthenticated(self):
    #     response = self.client.put(self.profile_url, {
    #         'first_name': 'UpdatedFirstName'
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_update_user_profile_invalid_data(self):
    #     # Authenticate the user
    #     self.client.force_authenticate(user=self.user)

    #     # Try updating with invalid phone number
    #     response = self.client.put(self.profile_url, {
    #         'phone_number': 'invalid_phone'
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('phone_number', response.data)

    # # Password Change Tests
    # def test_change_password_success(self):
    #     # Authenticate the user
    #     self.client.force_authenticate(user=self.user)

    #     # Change password
    #     change_password_url = reverse('change-password')  # Adjust to your endpoint
    #     response = self.client.put(change_password_url, {
    #         'old_password': self.user_data_for_login['password'],
    #         'new_password': 'NewStrongPassword456!',
    #         'new_password2': 'NewStrongPassword456!'
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('message', response.data)

    # def test_change_password_wrong_old_password(self):
        # Authenticate the user
        # self.client.force_authenticate(user=self.user)

        # Attempt to change password with an incorrect old password
        # change_password_url = reverse('change-password')  # Adjust to your endpoint
        # response = self.client.put(change_password_url, {
        #     'old_password': 'WrongOldPassword',
        #     'new_password': 'NewStrongPassword456!',
        #     'new_password2': 'NewStrongPassword456!'
        # })
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('old_password', response.data)

