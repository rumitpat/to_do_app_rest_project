from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from app.models import *
class TestTaskListingApiCase(TestCase):
    def setUp(self):
        self.task_name ='testtask'
        self.task_details ='demo'
        self.task_end_date ='2021-12-2'
        self.task_end_time ='1:2:12'
        self.credentials = {
            'username': 'testuser',
            'password': 'password123'
            }
        User.objects.create_user(**self.credentials)

    def test_task_listing_api_signal(self):
        login_response = self.client.post(reverse('login'), data= self.credentials)
        self.assertEqual(login_response.status_code, 200)
        token= login_response.data['token']
        num_token =Token.objects.count()
        
        #create task...
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('taskcreate'),data ={
            'task_name': self.task_name,
            'task_details': self.task_details,
            'task_end_date': self.task_end_date,
            'task_end_time': self.task_end_time,
        })
        response = client.post(reverse('taskcreate'),data ={
            'task_name': self.task_name,
            'task_details': self.task_details,
            'task_end_date': self.task_end_date,
            'task_end_time': self.task_end_time,
        })
        self.assertEqual(response.status_code, 201)
        data = TaskData.objects.all()
        self.assertEqual(data.count(), 2)

        #task listing...
        response = client.get(reverse('tasklist'))
        for d in data:
            user =d.user
        self.assertEqual(user.username,self.credentials["username"])
        self.assertEqual(response.status_code, 200)
