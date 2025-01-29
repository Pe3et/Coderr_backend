from django.db import models
from rest_framework.fields import MinValueValidator


class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='offers', blank=True, null=True)


class Feature(models.Model):
    name = models.CharField(max_length=200)


class OfferDetail(models.Model):
    OFFER_TYPES = (
        ('basic', 'BASIC'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    )

    title = models.CharField(max_length=200)
    revisions = models.IntegerField(default=0, validators=[MinValueValidator(-1)])
    delivery_time_in_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature, related_name='offers', blank=False)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')

    class Meta:
        unique_together = ('offer', 'offer_type')