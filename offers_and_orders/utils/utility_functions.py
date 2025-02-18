"""
get's all the offer details for an offer object.
It is used in the partial_update of the OffersViewSet. 
"""
def get_offer_details(offer_obj):
    details = offer_obj.details.prefetch_related('features')
    return [
        {
            'id': detail.id,
            'title': detail.title,
            'revisions': detail.revisions,
            'delivery_time_in_days': detail.delivery_time_in_days,
            'price': detail.price,  
            'offer_type': detail.offer_type,
            'features': [feature.name for feature in detail.features.all()]
        }
        for detail in details
    ]