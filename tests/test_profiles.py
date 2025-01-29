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
    Tests if registration with correct data for customers and businesses works as expected.
    """
    def test_successful_registration(self):
        customer_response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(customer_response.status_code, 201)

        correct_business_data = self.correct_customer_data
        correct_business_data['type'] = 'business'
        correct_business_data['username'] = 'testbusiness'
        correct_business_data['email'] = 'testbusiness@example.com'
        business_response = self.client.post(self.url, correct_business_data)
        self.assertEqual(business_response.status_code, 201)

    """
    Tests the expected behaviour of trying to register with duplicate data.
    """
    def test_duplicate_data(self):
        response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, self.correct_customer_data)
        self.assertEqual(response.status_code, 400)

    """
    Tests the expected behaviour of trying to register with incorrect data.
    """
    # def test_incorrect_data(self):
    #     pass

    """
    Tests the correct data structure of the response.
    """
    # def test_response_data_structure(self):
    #     pass

    """
    Tests any other request methods than POST.
    """
    # def test_other_request_methods(self):
    #     pass