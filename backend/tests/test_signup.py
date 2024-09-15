import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from backend.models import User




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

    user = User.objects.get(email=email)

    expected_data = {
        "user_id":user.user_id,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
    }

    response.data.pop('password', None)
    assert response.data == expected_data



@pytest.mark.django_db
def test_if_already_registered_email_return_400():
    first_name = 'jack'
    last_name = 'max'
    email = 'jackmax@gmail.com'
    password = 'password123'

    User.objects.create_user(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             password=password)


    client = APIClient()
    url = reverse('signup-signup')
    data = {
        'first_name':first_name,
        'last_name':last_name,
        'email':email,
        'password':password
    }

    response = client.post(url,data, format='json')
 
    assert response.status_code == status.HTTP_400_BAD_REQUEST