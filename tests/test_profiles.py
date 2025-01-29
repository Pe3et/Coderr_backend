from django.urls import reverse
from rest_framework.test import APITestCase


class TestProfiles(APITestCase):
    
    def test_registration_success(self):
        customer_data = {
            'username': 'testcustomer',
            'email': 'testcustomer@example.com',
            'password': 'password123',
            'repeated_password': 'password123',
            'type': 'customer'
        }
        business_data = {
            'username': 'testbusiness',
            'email': 'testbusiness@example.com',
            'password': 'password123',
            'repeated_password': 'password123',
            'type': 'business'
        }
        url = reverse('register')
        response = self.client.post(url, customer_data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(url, business_data)
        self.assertEqual(response.status_code, 201)

