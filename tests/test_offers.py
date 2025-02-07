from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.api.serializers import RegistrationSerializer
from offers_and_orders.api.models import Offer


class TestOffers(APITestCase):
    offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100.00,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }

    def setUp(self):
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
    Tests fully unauthorized offer POST.
    """
    def test_unauth_post_offer(self):
        url = reverse('offers-list')
        data = self.offer_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Tests customer unauthorized offer POST.
    """
    def test_unauth_post_offer(self):
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.customer_user)
        data = self.offer_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    Tests business authorized offer POST.
    """
    def test_auth_post_offer(self):
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.business_user)
        data = self.offer_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
    Tests GET offers list.
    """
    def test_get_offers_list(self):
        url = reverse('offers-list')
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Recalls the auth_post_offer and tests partial PATCH with new details containing new features.
    """
    def test_patch_offer_partial(self):
        self.test_auth_post_offer()
        url = reverse('offers-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.business_user)
        data = {
            'title': 'new package title',
            'details': [
                {
                'title': 'new basictitle',
                'features': ['newfeature', 'Visitenkarte'],
                'price': 1000,
                'revisions': 3,
                'delivery_time_in_days': 6,
                'offer_type': 'basic'
                }
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)