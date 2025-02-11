from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.api.serializers import RegistrationSerializer
from offers_and_orders.api.models import Offer
from tests import test_offers


class testOrders(APITestCase):

    def setUp(self):
        self.create_users()
        self.create_offer()

        
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
    Creates an offer to be able to test the ordering.
    """
    def create_offer(self):
        offer_data = test_offers.TestOffers.offer_data
        url = reverse('offers-list')

        self.client.force_authenticate(user=self.business_user)
        self.client.post(url, offer_data, format='json')
        self.client.force_authenticate(user=None)
        

    """
    Tests auth orders POST from customer_user.
    """
    def test_auth_post(self):
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.customer_user)
        post_data = { 'offer_detail_id': 1 }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ###erst offer erstellen 