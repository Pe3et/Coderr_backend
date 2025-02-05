from django.contrib import admin

from offers_and_orders.api.models import Feature, Offer, OfferDetail

# Register your models here.
admin.site.register(Offer)
admin.site.register(OfferDetail)
admin.site.register(Feature)