from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'],
                                            validated_data['email'],
                                            validated_data['password'])
            return user

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
