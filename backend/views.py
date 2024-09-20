from django.shortcuts import render
from .serializer import Signup
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#signup view
class SignupViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self,request):
            serializer = Signup(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_data= {"user_id": user.user_id, **serializer.data}
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
             'user_id': user.user_id,
             'email': user.email,
             'refresh': str(refresh),
             'access': access_token},
             status=status.HTTP_200_OK) 
    

class SomeSecureView(viewsets.ViewSet): 
     permission_classes = [IsAuthenticated]

     @action(detail=False, method=['get'])
     def secure_data(self,request):
          return Response({"data":"This is secured view!"})


