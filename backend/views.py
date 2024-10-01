from django.shortcuts import render
from .serializer import Signup, PostSerializer
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Post
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny


#signup view
class SignupViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self,request):
            serializer = Signup(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_data= {"id": user.id, **serializer.data}
                return Response(response_data, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#login view
class LoginViewSet(viewsets.ViewSet):

    @action(detail=False,methods=['post'])
    def login(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
             return Response({"error":"Kindly fill all the fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
             user = User.objects.get(email=email)
        except User.DoesNotExist:
             return Response({"error":"Invalid email or password"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
             return Response({"error":"Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
             'id': user.id,
             'email': user.email,
             'refresh': str(refresh),
             'access': access_token},
             status=status.HTTP_200_OK) 
    

class SomeSecureView(viewsets.ViewSet): 
     permission_classes = [IsAuthenticated]

     @action(detail=False, method=['get'])
     def secure_data(self,request):
          return Response({"data":"This is secured view!"})
     

# User Home Screen
class HomeViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

    def home(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response({
            "message": "WELCOME", 
            "posts": serializer.data, 
            "user": user.id 
        }, status=status.HTTP_200_OK)



class CreatePostViewSet(viewsets.ViewSet):
     # permission_classes = [IsAuthenticated]

     @action(detail=True, methods=['post'])
     def create_post(self,request, pk=None):
          user = User.objects.get(pk=pk)
          serializer = PostSerializer(data=request.data)

          if serializer.is_valid():
               serializer.save(user=user)
               return Response({"user":user.id,
                                "serializer":serializer.data,
                                },
                                status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class SinglePostViewSet(viewsets.ViewSet):
     
     @action(detail=True, method=['Get','Delete'])
     def single_post(self,request, pk=None, post_id=None):
          user = User.objects.get(pk=pk)
          post = Post.objects.get(pk=post_id, user=user)

          if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response({"user":user.id,
                                "post":serializer.data
                                },
                                status=status.HTTP_200_OK)
          
          if request.method == 'DELETE':
               post.delete()
               return Response({'message',f'post {post.post_text} deleted successfully'},
                               status=status.HTTP_200_OK)
     
        