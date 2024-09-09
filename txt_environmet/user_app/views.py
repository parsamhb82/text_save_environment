from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serilizers import UserRegisterSerializer, UserSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
class Login(TokenObtainPairView):
    pass

class Refresh(TokenRefreshView):
    pass

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    def perform_create(self, serializer):
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
