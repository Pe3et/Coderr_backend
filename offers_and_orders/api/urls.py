from django.urls import include, path
from rest_framework import routers

from offers_and_orders.api.views import OfferViewSet


router = routers.SimpleRouter()
router.register(r'offers', OfferViewSet, basename='offers')

urlpatterns = [
    path('', include(router.urls)),
]