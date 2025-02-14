from django.urls import include, path
from rest_framework import routers

from offers_and_orders.api.views import OfferViewSet, OrderViewSet, ReviewViewSet, base_info_view, completedOrderCount, offerdetailsView, openOrderCount


router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', offerdetailsView, name='offerdetail-detail'),
    path('order-count/<int:business_user_id>/', openOrderCount, name='open-order-count'),
    path('completed-order-count/<int:business_user_id>/', completedOrderCount, name='completed-order-count'),
    path('base-info/', base_info_view, name='base-info')
]