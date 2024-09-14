from django.shortcuts import render
from .serializer import Signup
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
# Create your views here.


#signuo view
class SignupViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self,request):
            serializer = Signup(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        