from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from .models import User
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def getRoutes(request):
    routes = [
        "api/token",
        "api/token/refresh",
    ]

    return Response(routes)

# Register User


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.serializer_class(data=payload, many=False)
        if serializer.is_valid():
            username = payload["username"]
            email = payload["email"]
            firstname = payload["first_name"]
            lastname = payload["last_name"]
            password = payload["password"]

            emailExists = User.objects.filter(email=email).exists()
            usernameExists = User.objects.filter(username=username).exists()
            if emailExists or usernameExists:
                return Response({"error": "Email or username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            hashedPassword = make_password(password)

            newUser = {"username": username,
                       "email": email,
                       "first_name": firstname,
                       "last_name": lastname,
                       "password": hashedPassword,
                       "is_active": True,
                       "is_staff": False}
            user = User.objects.create_user(newUser)
            info = {"Success": "User created successfully"}
            return Response(info, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        payload = request.data
        username = payload['username']
        password = payload['password']
        if username is None:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return Response({"error":"User with the given username doesn't exists"},status=status.HTTP_400_BAD_REQUEST)

        is_authenticated = check_password(password,user.password)
        if is_authenticated:
            payload = {
                'id': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY)
            response_info = {
                "token": token
            }
            return Response(response_info, status=status.HTTP_200_OK)
            return Response({"success": "Authentication successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
