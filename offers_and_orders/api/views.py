from django.shortcuts import render
from rest_framework import viewsets

from offers_and_orders.api.models import Offer
from offers_and_orders.api.serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer