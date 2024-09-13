from rest_framework import serializers
from .models import User


class Signup(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_image','first_name','last_name','email','password']
    
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        print(user.email,user.first_name)
        return user
    
    def validate(self,data):
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"User with this email already exists"})
        
        return data








        
