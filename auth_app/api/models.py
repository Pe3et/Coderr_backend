from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')