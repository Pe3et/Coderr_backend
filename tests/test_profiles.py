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
    Tests if the single GET functions properly.
    """
    def test_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        print(url)
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        