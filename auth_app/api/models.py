from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=20, blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    working_hours = models.CharField(max_length=5, blank=True, null=True)
    