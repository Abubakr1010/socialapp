import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse




@pytest.mark.django_db
def test_if_user_signedin_return_201():
    first_name = 'jack'
    last_name = 'max'
    email = 'email@gmail.com'
    password = 'password123'


    client = APIClient()
    url = reverse('signup-signup')
    data = {'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'password':password
    }
    
    response = client.post(url, data, format = 'json')

    assert response.status_code == status.HTTP_201_CREATED



