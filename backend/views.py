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
     

class HomeViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

    def home(self, request, login_pk=None):
        try:
            # Fetch the user from the provided login_pk
            user = User.objects.get(pk=login_pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Now filter the posts by this user
        posts = Post.objects.filter(user=user)
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        # Return the response with user data and posts
        return Response({
            "message": "WELCOME", 
            "posts": serializer.data, 
            "user": user.username  # You can return user info here
        }, status=status.HTTP_200_OK)



class CreatePostViewSet(viewsets.ViewSet):
     # permission_classes = [IsAuthenticated]

     @action(detail=True, methods=['post'])
     def create_post(self,request, login_pk=None):
          serializer = PostSerializer(data=request.data)

          if serializer.is_valid():
               serializer.save(user=request.user)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     


     
