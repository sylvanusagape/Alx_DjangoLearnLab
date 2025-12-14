from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

<<<<<<< HEAD
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer
)
=======
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
>>>>>>> 7d6f437


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
<<<<<<< HEAD

        token, _ = Token.objects.get_or_create(user=user)

=======
        token, _ = Token.objects.get_or_create(user=user)
>>>>>>> 7d6f437
        return Response({
            'token': token.key,
            'user': serializer.data
        })


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
<<<<<<< HEAD

        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })
=======
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
>>>>>>> 7d6f437


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
