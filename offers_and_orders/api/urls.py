from django.urls import include, path
from rest_framework import routers

from offers_and_orders.api.views import OfferViewSet, OrderViewSet, offerdetailsView


router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', offerdetailsView, name='offerdetail-detail'),
]