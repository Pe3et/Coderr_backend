from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestLogin(APITestCase):
    url = reverse('login')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@mail.de'
        )

    """
    Test if login is working properly.
    """
    def test_correct_login(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'token': Token.objects.get(user=self.user).key,
            'username': self.user.username,
            'email': self.user.email,
            'user_id': self.user.id
        })

    """
    Tests if a bad login fails correctly.
    """
    def test_failed_login(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, {'non_field_errors:': ['Falsche Anmeldedaten.']})

    """
    Test Guest logins.
    """
    def test_guest_logins(self):
        customer_guest = {
            'username': 'andrey',
            'password': 'asdasd'
        }
        business_guest = {
            'username': 'kevin',
            'password': 'asdasd24'
        }

        response = self.client.post(self.url, customer_guest)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'token': Token.objects.get(user=User.objects.get(username='andrey')).key,
            'username': 'andrey',
            'email': 'testcustomer@mail.de',
            'user_id': User.objects.get(username='andrey').id
        })

        response = self.client.post(self.url, business_guest)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'token': Token.objects.get(user=User.objects.get(username='kevin')).key,
            'username': 'kevin',
            'email': 'testbusiness@mail.de',
            'user_id': User.objects.get(username='kevin').id
        })

    """
    Tests any other request methods than POST.
    """
    def test_other_request_methods(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

        response = self.client.put(self.url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(self.url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 405)
