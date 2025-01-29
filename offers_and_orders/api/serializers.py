from rest_framework import serializers

from offers_and_orders.api.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

