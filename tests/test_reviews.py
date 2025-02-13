from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.api.serializers import RegistrationSerializer


class TestReviews(APITestCase):

    def setUp(self):
        self.create_users()

    """
    Creates a customer_user and a business_user for testing.
    """
    def create_users(self):
        business_user_data = {
            'username': 'offers_business_testuser',
            'email': 'offers_business_testuser@example.com',
            'password': 'password',
            'repeated_password': 'password',
            'type': 'business'
        }
        serializer = RegistrationSerializer(data=business_user_data)
        serializer.is_valid(raise_exception=True)
        self.business_user = serializer.save()

        customer_user_data = {
            'username': 'offers_customer_testuser',
            'email': 'offers_customer_testuser@example.com',
            'password': 'password',
            'repeated_password': 'password',
            'type': 'customer'
        }
        serializer = RegistrationSerializer(data=customer_user_data)
        serializer.is_valid(raise_exception=True)
        self.customer_user = serializer.save()
    
    """
    Tests authorized review POST.
    """
    def test_authorized_review_post(self):
        url = reverse('reviews-list')
        review_test_data = {
            'business_user': self.business_user.id,
            'description': 'test',
            'rating': 5
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(url, review_test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
    Tests general unathorized review POST.
    """
    def test_unauthorized_review_post(self):
        url = reverse('reviews-list')
        review_test_data = {
            'business_user': self.business_user.id,
            'description': 'test',
            'rating': 5
        }
        response = self.client.post(url, review_test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Tests bad review POST.
    """
    def test_bad_review_post(self):
        url = reverse('reviews-list')
        bad_review_test_data = {
            'business_user': self.business_user.id,
            'description': 'test',
            'rating': 6
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(url, bad_review_test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Tests review POST coming from a business, which is not allowed.
    """
    def test_review_post_from_business(self):
        url = reverse('reviews-list')
        review_test_data = {
            'business_user': self.business_user.id,
            'description': 'test',
            'rating': 5
        }
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(url, review_test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)