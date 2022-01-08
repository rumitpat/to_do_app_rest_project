from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


class TestUserLoginApiCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'password123'
            }
        User.objects.create_user(**self.credentials)

    def test_invalid(self):
        payload = None
        response = self.client.post(reverse("login"), data=payload)
        self.assertNotEqual(response.status_code, 200)

        payload = {}
        response = self.client.post(reverse("login"), data=payload)
        self.assertNotEqual(response.status_code, 200)

        payload = {
            'username': 'wrong',
            'password': 'password123',
        }
        response = self.client.post(reverse("login"), data=payload)
        self.assertNotEqual(response.status_code, 200)

        payload = {
            'username': 'testuser',
            'password': 'wrong',
        }
        response = self.client.post(reverse("login"), data=payload)
        self.assertNotEqual(response.status_code, 200)

    def test_user_login_api_signal(self):
        response = self.client.post(reverse('login'), data= self.credentials)
        self.assertEqual(response.status_code, 200)

