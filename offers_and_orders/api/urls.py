from django.urls import include, path
from rest_framework import routers

from offers_and_orders.api.views import OfferViewSet, OrderViewSet, ReviewViewSet, completedOrderCount, offerdetailsView, openOrderCount


router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', offerdetailsView, name='offerdetail-detail'),
    path('order-count/<business_user_id>', openOrderCount, name='open-order-count'),
    path('completed-order-count/<business_user_id>', completedOrderCount, name='completed-order-count')
]