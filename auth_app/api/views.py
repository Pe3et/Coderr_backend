from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.models import UserProfile
from auth_app.api.serializers import RegistrationSerializer, UserProfileSerializer
from auth_app.utils import guest_logins


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        guest_logins.check_guest_logins()
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'email': user.email,
                'username': user.username,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'non_field_errors:': ['Falsche Anmeldedaten.']}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'email': saved_account.email,
                'username': saved_account.username,
                'user_id': saved_account.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class SingleProfileView(APIView):

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        data = serializer.data
        data.update({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.date_joined
        })
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pass
