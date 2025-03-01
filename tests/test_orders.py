from django.urls import reverse
from rest_framework import status
from rest_framework.fields import parse_datetime
from rest_framework.test import APITestCase

from auth_app.api.serializers import RegistrationSerializer
from offers_and_orders.api.models import Offer, Order
from tests import test_offers


class TestOrders(APITestCase):

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
        order = Order.objects.get(id=1)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['customer_user'], 2)
        self.assertEqual(response.data['business_user'], 1)
        self.assertEqual(response.data['title'], 'Basic Design')
        self.assertEqual(response.data['revisions'], 2)
        self.assertEqual(response.data['delivery_time_in_days'], 5)
        self.assertEqual(float(response.data['price']), 100.00)
        self.assertEqual(response.data['features'], ['Logo Design', 'Visitenkarte'])
        self.assertEqual(response.data['offer_type'], 'basic')
        self.assertEqual(response.data['status'], 'in_progress')
        self.assertEqual(parse_datetime(response.data['created_at']), order.created_at)
        self.assertEqual(parse_datetime(response.data['updated_at']), order.updated_at)

    """
    Tests business user trying to POST, which is not wanted. 
    """
    def test_business_post(self):
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.business_user)
        post_data = { 'offer_detail_id': 1 }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Tests list GET.
    """
    def test_list_get(self):
        url = reverse('orders-list')
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Tests the partial status PATCH of an offer from the business_user.
    """
    def test_status_patch(self):
        self.test_auth_post()
        url = reverse('orders-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.business_user)
        patch_data = { 'status': 'completed' }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    """
    Tests a bad PATCH from a business_user.
    """
    def test_bad_business_patch(self):
        self.test_auth_post()
        url = reverse('orders-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.business_user)
        patch_data = { 'title': 'test bad patch' }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Tests the partial status PATCH from a customer_user.
    """
    def test_unauth_patch(self):
        self.test_auth_post()
        url = reverse('orders-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.customer_user)
        patch_data = { 'status': 'completed' }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Tests open business orders count endpoint.
    """
    def test_open_business_orders_count(self):
        self.test_auth_post()
        url = reverse('open-order-count', kwargs={'business_user_id': self.business_user.id})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], Order.objects.filter(status='in_progress').count())

    """
    Tests open business orders count endpoint with business user not existing.
    """
    def test_open_business_orders_count_not_found(self):
        self.test_auth_post()
        url = reverse('open-order-count', kwargs={'business_user_id': self.customer_user.id})
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Business user not found.')

    """
    Tests completed business orders count endpoint.
    """
    def test_completed_business_orders_count(self):
        self.test_status_patch()
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business_user.id})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], Order.objects.filter(status='completed').count())

    """
    Tests completed business orders count endpoint with business user not existing.
    """
    def test_completed_business_orders_count_not_found(self):
        self.test_status_patch()
        url = reverse('completed-order-count', kwargs={'business_user_id': self.customer_user.id})
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Business user not found.')