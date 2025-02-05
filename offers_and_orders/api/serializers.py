from django.db.models import Min
from rest_framework import serializers

from offers_and_orders.api.models import Feature, Offer, OfferDetail


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class OfferDetailSerializer(serializers.ModelSerializer):
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = OfferDetail
        exclude = ['offer']

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        offer_detail = OfferDetail.objects.create(**validated_data)

        features = []
        for feature_name in features_data:
            feature, created = Feature.objects.get_or_create(name=feature_name)
            features.append(feature)

        offer_detail.features.set(features)
        return offer_detail


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']

    """
    Handles the creation of an offer with all it's details and their features.
    """
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(creator=user, **validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features', [])
            offer_detail = OfferDetail.objects.create(offer=offer, **detail_data)

            for feature_name in features_data:
                feature, created = Feature.objects.get_or_create(name=feature_name)
                offer_detail.features.add(feature)
            
        offer.min_price = self.get_min_price(offer)
        offer.save()
        return offer
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.min_price = self.get_min_price(instance)
        instance.save()
        return instance
    
    """
    Gets the min_price of the related OfferDetails.
    """
    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']