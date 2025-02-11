from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.models import UserProfile
from offers_and_orders.api.models import Offer, OfferDetail, Order
from offers_and_orders.api.permissions import IsBusinessAndOwnerOrAdmin, IsCustomer, IsSuperuser
from offers_and_orders.api.serializers import OfferDetailSerializer, OfferSerializer, OrderSerializer


class OfferFilter(FilterSet):
    creator_id = NumberFilter(field_name='user__id')
    min_price = NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = NumberFilter(field_name='min_delivery_time', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['min_price', 'max_delivery_time', 'creator_id']


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('id')
    serializer_class = OfferSerializer
    filterset_class = OfferFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

    """
    Only business users or superusers are allowed to change offers.
    """
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsBusinessAndOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    """
    Handles formatting the list GET.
    """
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

            user = Offer.objects.get(id=item['id']).user
            item['user_details'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username
            }
    
        return data
    
    """
    Handles the creation.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    """
    Adds user-details to the single view response.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        user = instance.user
        data['user_details'] = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }
        
        return Response(data)
    
    """
    Handles the PATCH.
    """
    def partial_update(self, request, *args, **kwargs):
        offer_obj = self.get_object()
        new_offer_detail_data = request.data['details'][0]
        offer_type = new_offer_detail_data['offer_type']
        offer_detail_obj = OfferDetail.objects.get(offer=offer_obj, offer_type=offer_type)
        serializer = OfferDetailSerializer(offer_detail_obj, data=new_offer_detail_data, partial=True)
        if serializer.is_valid():
            offer_detail = serializer.save()

            response_data = {
                'id': offer_obj.id,
                'title': offer_obj.title,
                'details': OfferDetailSerializer(offer_detail).data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Handles custom delete logic.
    """    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {}
        return Response(data, status=status.HTTP_200_OK)


"""
Function based view for the single offerdetails endpoint.
"""
@api_view(['GET'])
def offerdetailsView(request, pk):
    try:
        offer_detail = OfferDetail.objects.get(pk=pk)
    except OfferDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OfferDetailSerializer(offer_detail)
    return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

    """
    Only customer users are allowed to create orders and change the status.
    Only admins are allowed to delete orders.
    """
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'partial_update']:
            permission_classes = [IsCustomer]
        else:
            permission_classes = [IsSuperuser]
        
        return [permission() for permission in permission_classes]
    
    """
    Returns only the orders related to the requesting users.
    """
    def list(self, request, *args, **kwargs):
        try:
            userProfile = UserProfile.objects.get(user=request.user)
            if userProfile.type == 'customer':
                queryset = Order.objects.filter(customer_user=request.user)
            elif userProfile.type == 'business':
                queryset = Order.objects.filter(business_user=request.user)
            else:
                queryset = Order.objects.none()

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    """
    Only user realted orders can be retrieved.
    """
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        if order.customer_user == request.user or order.business_user == request.user:
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({}, status=status.HTTP_200_OK)