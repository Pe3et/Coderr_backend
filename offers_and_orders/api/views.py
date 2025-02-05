from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.response import Response

from offers_and_orders.api.models import Offer
from offers_and_orders.api.serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filterset_fields = ['min_price']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.modify_list_data(serializer.data)
            return self.get_paginated_response(data)
        
        serializer = self.get_serializer(queryset, many=True)
        data = self.modify_list_data(serializer.data)
        return Response(data, status=status.HTTP_200_OK)
    
    """
    To modify the representation of the offer-details in the list response.
    """
    def modify_list_data(self, data):
        for item in data:
            item['details'] = [
                {"id": detail.id, "url": reverse('offers-detail', kwargs={'pk': detail.id})}
                for detail in Offer.objects.get(id=item['id']).details.all()
            ]
        return data