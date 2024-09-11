from rest_framework import serializers
from .models import User


class Signup(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_image','first_name','last_name','email','password']



        
