from django.urls import reverse
from rest_framework.test import APITestCase

from auth_app.api.serializers import RegistrationSerializer


class TestProfiles(APITestCase):

    def setUp(self):
        test_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'repeated_password': 'password',
            'type': 'customer'
        }
        serializer = RegistrationSerializer(data=test_user_data)
        serializer.is_valid(raise_exception=True)
        self.user = serializer.save()

    """
    Tests if the unauthorized single GET raised 403 Forbidden error.
    """
    def test_unauth_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 403)

    """
    Tests if the authorized single GET functions properly.
    """
    def test_auth_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        