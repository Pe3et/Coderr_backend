from django.shortcuts import render
from rest_framework import viewsets

from offers_and_orders.api.models import Offer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()