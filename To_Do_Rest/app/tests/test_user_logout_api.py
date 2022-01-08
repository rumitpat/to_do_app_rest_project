from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class TestUserLogoutApiCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'password123'
            }
        User.objects.create_user(**self.credentials)

    def test_user_logout_api_signal(self):
        #user login
        login_response = self.client.post(reverse('login'), data= self.credentials)
        self.assertEqual(login_response.status_code, 200)
        token= login_response.data['token']
        num_token =Token.objects.count()

        #user logout
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data is not None)
        self.assertEqual(num_token - 1, Token.objects.count())

        

