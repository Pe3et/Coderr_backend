from django.contrib.auth.models import User
from django.db import models
from rest_framework.fields import MaxValueValidator, MinValueValidator


class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='offer_pictures', null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class OfferDetail(models.Model):
    OFFER_TYPES = (
        ('basic', 'BASIC'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    )

    title = models.CharField(max_length=200)
    revisions = models.IntegerField(validators=[MinValueValidator(-1)])
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature, related_name='offers', blank=False)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')

    class Meta:
        unique_together = ('offer', 'offer_type')

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_TYPES = (
        ('in_progress', 'IN_PROGRESS'),
        ('completed', 'COMPLETED'),
        ('cancelled', 'CANCELLED'),
    )

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_orders')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.offer_detail.title
    

class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_business')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewing_customer')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewer.username} bewertete {self.business_user.username}"