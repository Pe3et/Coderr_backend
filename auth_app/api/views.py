from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
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


@api_view(['GET', 'PATCH'])
def single_profile_view(request, pk):
    pass
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)
        if profile:
            serializer = UserProfileSerializer(profile)
            data = serializer.data
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['email'] = user.email
            data['created_at'] = user.date_joined
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'non_field_errors': 'Profil nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)