from rest_framework import serializers
from .models import User, Post, Comment


# Signup Serializer
class Signup(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
    
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        print(user.email,user.first_name)
        return user
    
    def validate(self,data):
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"User with this email already exists"})
        
        password = data.get('password')
        if len(password) < 7:
            return serializers.ValidationError({"password":"Password must be at least 7 character long "})
        
        return data
    



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','profile_imagemy']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['user_id','comment_id', 'text']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id','post_text','post_image','created','likes','likes_count','comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

    

    








        
