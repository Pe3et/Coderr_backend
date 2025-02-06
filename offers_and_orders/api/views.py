from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from auth_app.api.models import UserProfile
from offers_and_orders.api.models import Offer, OfferDetail
from offers_and_orders.api.serializers import OfferDetailSerializer, OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('id')
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
    To modify the representation of the offer-details in the list response
    and adds user_details.
    """
    def modify_list_data(self, data):
        for item in data:
            item['details'] = [
                {'id': detail.id, 'url': reverse('offers-detail', kwargs={'pk': detail.id})}
                for detail in Offer.objects.get(id=item['id']).details.all()
            ]

            creator = Offer.objects.get(id=item['id']).user
            item['user_details'] = {
                'first_name': creator.first_name,
                'last_name': creator.last_name,
                'username': creator.username
            }
    
        return data
    
    """
    To ensure only business users can create new offers.
    """
    def create(self, request, *args, **kwargs):
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.type == 'business': 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("Nur Anbieter dürfen Angebote erstellen.")
        
    """
    Adds user-details to the single view response.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        creator = instance.user
        data['user_details'] = {
            'first_name': creator.first_name,
            'last_name': creator.last_name,
            'username': creator.username
        }
        
        return Response(data)
    
    """
    Handles the PATCH.
    """
    # def partial_update(self, request, *args, **kwargs):
    #     offer = Offer.objects.get(title=request.data['title'])
    #     offer_type = request.data['type']


@api_view(['GET'])
def offerdetailsView(request, pk):
    try:
        offer_detail = OfferDetail.objects.get(pk=pk)
    except OfferDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OfferDetailSerializer(offer_detail)
    return Response(serializer.data)