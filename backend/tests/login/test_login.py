import pytest
from backend.models import User
from rest_framework.test import APITestCase
from rest_framework import status



class LoginViewSetTest(APITestCase):

    def setUp(self):
        # This method runs before each test
        self.create_user()
        self.login_url = '/login/login/'

    def create_user(self):
        self.user = User.objects.create_user(
                               first_name='jack',
                               last_name='max',
                               email = 'jackmax@gmail.com',
                               password = 'password123'
        )

    def test_login_successfull_return_200(self):
        data={
            'email': 'jackmax@gmail.com',
            'password':'password123'
        }

        response = self.client.post(self.login_url,data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password_return_400(self):
        data ={
            'email':'jackmax@gmail.com',
            'password':'password122'
        }

        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




