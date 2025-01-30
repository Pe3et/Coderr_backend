import copy
from django.urls import reverse
from rest_framework.test import APITestCase


class TestRegistration(APITestCase):
    url = reverse('register')
    correct_customer_data = {
        'username': 'testcustomer',
        'email': 'testcustomer@example.com',
        'password': 'password123',
        'repeated_password': 'password123',
        'type': 'customer'
    }

    """
    Tests the expected behaviour of trying to register with duplicate data.
    """
    def test_duplicate_data(self):
        response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 400)

    """
    Tests if registration with correct data for customers and businesses works as expected.
    """
    def test_successful_registration(self):
        self.correct_customer_data['username'] = 'testcustomer2'
        self.correct_customer_data['email'] = 'testcustomer2@example.com'
        customer_response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(customer_response.status_code, 201)

        correct_business_data = copy.deepcopy(self.correct_customer_data)
        correct_business_data['type'] = 'business'
        correct_business_data['username'] = 'testbusiness'
        correct_business_data['email'] = 'testbusiness@example.com'
        business_response = self.client.post(self.url, correct_business_data)
        self.assertEqual(business_response.status_code, 201)

    """
    Tests the expected behaviour of trying to register with incorrect type.
    """
    def test_incorrect_type(self):
        incorrect_data = copy.deepcopy(self.correct_customer_data)
        incorrect_data['username'] = 'incorrect_type_user'
        incorrect_data['email'] = 'incorrect@type.de'
        incorrect_data['type'] = 'incorrect_type'
        response = self.client.post(self.url, incorrect_data)
        self.assertEqual(response.status_code, 400)

    """
    Tests any other request methods than POST.
    """
    def test_other_request_methods(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

        response = self.client.put(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 405)