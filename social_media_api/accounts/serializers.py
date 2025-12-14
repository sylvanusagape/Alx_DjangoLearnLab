from rest_framework import serializers
<<<<<<< HEAD
from django.contrib.auth import authenticate
from .models import User
=======
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()
>>>>>>> 7d6f437


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
<<<<<<< HEAD
=======
        Token.objects.create(user=user)
>>>>>>> 7d6f437
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class UserProfileSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    followers_count = serializers.IntegerField(
        source='followers.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'bio',
            'profile_picture',
            'followers_count'
        ]
=======
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers_count']
>>>>>>> 7d6f437
