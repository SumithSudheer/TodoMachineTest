from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/auth/token/'
        self.profile_url = '/api/users/profile/'
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPass123',
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_get_profile(self):
        # Register user first
        self.client.post(self.register_url, self.user_data)
        # Login
        login_resp = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'TestPass123'
        })
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        access_token = login_resp.data['access']

        # Get profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_resp = self.client.get(self.profile_url)
        self.assertEqual(profile_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_resp.data['email'], 'test@example.com')
