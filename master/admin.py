from django.contrib import admin
from master.models import (
    BrandType,
    masterAvatarProfile,
    gender,
    music_type,
    drink_type,
    bar_type,
    property_type,
    Country,
    State,
    City,
    PaymentMethod,
    PropertyFacilities,
    ArtistType,
    Language,
    AdditionalFeature,
    DealTermsAndConditions,
    FlashDealFor,
    BrandType,
    DealType,
    EntryType,
    Occasion,
)

# Register your models here.


admin.site.register(masterAvatarProfile)
admin.site.register(gender)
admin.site.register(music_type)
admin.site.register(drink_type)
admin.site.register(bar_type)
admin.site.register(property_type)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(PaymentMethod)
admin.site.register(PropertyFacilities)
admin.site.register(ArtistType)
admin.site.register(Language)
admin.site.register(AdditionalFeature)
admin.site.register(DealTermsAndConditions)
admin.site.register(FlashDealFor)
admin.site.register(BrandType)
admin.site.register(DealType)
admin.site.register(EntryType)
admin.site.register(Occasion)
