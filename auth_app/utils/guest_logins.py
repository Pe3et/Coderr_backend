from django.contrib.auth.models import User

from auth_app.api.serializers import RegistrationSerializer

"""
Checks if the guest logins already exist in the Database and calls creation of them if not.
"""
def check_guest_logins():
    if not User.objects.filter(username='andrey').exists():
        create_customer_guest_account()
    if not User.objects.filter(username='kevin').exists():
        create_business_guest_account()

"""
Creates the guest account for customer testing.
"""
def create_customer_guest_account():
    customer_guest_data = {
        'username': 'andrey',
        'email': 'testcustomer@mail.de',
        'password': 'asdasd',
        'repeated_password': 'asdasd',
        'type': 'customer'
    }
    serializer = RegistrationSerializer(data=customer_guest_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

"""
Creates the guest account for business testing.
"""
def create_business_guest_account():
    business_guest_data = {
        'username': 'kevin',
        'email': 'testbusiness@mail.de',
        'password': 'asdasd24',
        'repeated_password': 'asdasd24',
        'type': 'business'
    }
    serializer = RegistrationSerializer(data=business_guest_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
