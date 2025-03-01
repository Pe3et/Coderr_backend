from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=20, blank=False, default="")
    file = models.FileField(blank=True, null=True, upload_to='profile_pictures/')
    description = models.TextField(blank=False, default="")
    tel = models.CharField(max_length=20, blank=False, default="")
    working_hours = models.CharField(max_length=30, blank=False, default="")
    uploaded_at = models.DateTimeField(auto_now=True, null=True)