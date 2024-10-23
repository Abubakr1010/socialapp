import pytest
from rest_framework.test import APITestCase
from backend.models import User, Post
from rest_framework import status




class TestSettingsSiewset(APITestCase):

    def setUp(self) -> None:
        self.create_user()

        self.settings_url= f'/update_name/{self.user.id}/'

    def create_user(self):
        self.user=User.objects.create_user(
            first_name = 'max',
            last_name = 'jack',
            email = 'maxjack@gmail.com',
            password = 'password123'
        )
        
    def test_update_name_return_200(self):
        data={
            "first_name":"Tim",
            "last_name":"Tate"
        }

        response = self.client.put(self.settings_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



