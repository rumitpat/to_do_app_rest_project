from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


class TestUserRegisterApiCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.first_name = 'first_name'
        self.last_name = 'last_name'
        self.password ='password'

    def test_invalid(self):

        payload = None
        response = self.client.post(reverse("signup"), data=payload)
        self.assertNotEqual(response.status_code, 201)

        payload = {}
        response = self.client.post(reverse("signup"), data=payload)
        self.assertNotEqual(response.status_code, 201)

        payload = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }
        response = self.client.post(reverse("signup"), data=payload)
        self.assertNotEqual(response.status_code, 201)

        payload = {
            'wrong': self.username,
            'wrong': self.email,
            'wrong': self.password,
        }
        response = self.client.post(reverse("signup"), data=payload)
        self.assertNotEqual(response.status_code, 201)

         

    def test_user_register_api_signal(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name':self.first_name,
            'last_name':self.last_name
            })
        self.assertEqual(response.status_code, 201)

    def test_duplicate(self):
        payload = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name':self.first_name,
            'last_name':self.last_name
        }
        response = self.client.post(reverse('signup'), data=payload)
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('signup'), data =payload) 
        self.assertNotEqual(response.status_code, 201)
