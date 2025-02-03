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
    GET single profile
    """
    """
    Tests if the unauthorized single GET raised 403 Forbidden error.
    """
    def test_unauth_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    """
    Tests if the authorized single GET functions properly.
    """
    def test_auth_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """
    Tests the functionality for handling the try to GET a user, which doesn't exist.
    """
    def test_auth_non_existing_single_profile_get(self):
        url = reverse('profile-detail', kwargs={'pk':13337})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    """
    PATCH single profile
    """
    """
    Tests the authorized single profile PATCH request.
    """
    def test_auth_single_profile_patch(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, { 'first_name': 'test'})
        self.assertEqual(response.status_code, 200)

    """
    Tests the unauthorized single profile PATCH request.
    """
    def test_unauth_single_profile_patch(self):
        pass
        
    """
    Tests a bad single profile PATCH request.
    """
    def test_bad_single_profile_patch(self):
        url = reverse('profile-detail', kwargs={'pk':self.user.id})
        self.client.force_authenticate(user=self.user)

    """
    Tests to PATCH a non-existing user profile.
    """
    def test_hacking_single_profile_patch(self):
        url = reverse('profile-detail', kwargs={'pk':13337})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, { 'first_name': 'test'})
        self.assertEqual(response.status_code, 404)

    """
    Tests a hacking attempt with Token from another user to PATCH another users profile.
    """
    def test_hacking_single_profile_patch(self):
        pass

