from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


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


@api_view(["GET"])
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
            user = User.objects.create(**newUser)
            info = {"Success": "User created successfully"}
            return Response(info, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        payload = request.data
        email = request.data.get('email')
        password = request.data.get('password')
        if email is not None:
            return Response({"username is required"}, status=status.HTTP_400_BAD_REQUEST)
        if password is not None:
            return Response({'password required'}, status=status.HTTP_401_UNAUTHORIZED)
            email = payload["email"]
            password = payload["password"]
            is_authenticated = authenticate(email = email, password = password)
