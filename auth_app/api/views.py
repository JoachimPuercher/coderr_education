from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer

class RegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        token, create = Token.objects.get_or_create(user=new_user)
        data = {
            'token' : token.key,
            'username' : new_user.username,
            'email' : new_user.email,
            'user_id' : new_user.pk
        }

        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=login_user)
        data = {
            'token' : token.key,
            'username' : login_user.username,
            'email' : login_user.email,
            'user_id' : login_user.pk
        }

        return Response(data, status=status.HTTP_200_OK)