import pytest
from rest_framework.test import APITestCase
from backend.models import User, Post
from rest_framework import status




class TestSinglePostView(APITestCase):

    def setUp(self) -> None:
        self.create_user()
        self.create_post()
        self.single_post_url= f'/single_post/{self.user.id}/{self.post.post_id}/'


    def create_user(self):
        self.user=User.objects.create_user(
            first_name = 'max',
            last_name = 'jack',
            email = 'maxjack@gmail.com',
            password = 'password123'
        )

    def create_post(self):
        self.post = Post.objects.create(
            post_text = 'hello world',
            user=self.user 
        )

    def test_update_post_return_200(self):
        data = {
            "post_text":"new updated world"
        }

        response = self.client.put(self.single_post_url, data, format='json')
 
        self.assertEqual(response.status_code, status.HTTP_200_OK)






