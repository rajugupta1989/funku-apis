from unicodedata import category
from django.db import models
from common.abstract_model import CommonAbstractModel
from account.models import User, FileRepo
from artist.models import UserAtrist
from master.models import (
    Country,
    State,
    City,
    PaymentMethod,
    PropertyFacilities,
    FlashDealFor,
    DealTermsAndConditions,
    drink_type,
    BrandType,
    DealType,
    EntryType,
    property_type
)




class UserProperty(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True
    )
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    opening_time = models.CharField(max_length=100, blank=True, null=True)
    closing_time = models.CharField(max_length=100, blank=True, null=True)
    payment = models.ManyToManyField(PaymentMethod, blank=True)
    total_capacity = models.IntegerField(blank=True, null=True)
    seating_capacity = models.IntegerField(blank=True, null=True)
    property_type = models.ForeignKey(property_type, on_delete=models.CASCADE, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    manager = models.ManyToManyField(User,related_name='manager', blank=True)
    listing_date = models.DateField(blank=True, null=True) 


class UserPropertyThumb(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to="documents", null=True, default=None)


class PropertyAvailableFacilities(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(PropertyFacilities, blank=True)


class PropertySocialDetail(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    exterior_instagram = models.CharField(max_length=100, blank=True, null=True)
    exterior_facebook = models.CharField(max_length=100, blank=True, null=True)
    exterior_gallery = models.ManyToManyField(
        FileRepo, blank=True, related_name="exterior_gallery"
    )
    interior_instagram = models.CharField(max_length=100, blank=True, null=True)
    interior_facebook = models.CharField(max_length=100, blank=True, null=True)
    interior_gallery = models.ManyToManyField(
        FileRepo, blank=True, related_name="interior_gallery"
    )
    menu_place = models.ManyToManyField(FileRepo, blank=True, related_name="menu_place")
    instagram = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    promoter = models.ManyToManyField(User, blank=True, related_name="promoter")
    



class FlashDealDetail(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    deal_name = models.CharField(max_length=100,blank=True, null=True)
    deal_for = models.ForeignKey(
        FlashDealFor, on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    terms_conditions = models.ManyToManyField(DealTermsAndConditions, blank=True)
    category = models.ForeignKey(
        drink_type, on_delete=models.CASCADE, blank=True, null=True
    )
    brand = models.ForeignKey(
        BrandType, on_delete=models.CASCADE, blank=True, null=True
    )


class Deal(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    deal_name = models.CharField(max_length=100,blank=True, null=True)
    deal_code = models.CharField(max_length=100,blank=True, null=True)
    deal_type = models.ForeignKey(
        DealType, on_delete=models.CASCADE, blank=True, null=True
    )
    deal_for = models.ForeignKey(
        FlashDealFor, on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    terms_conditions = models.ManyToManyField(DealTermsAndConditions, blank=True)
    entry_type = models.ForeignKey(
        EntryType, on_delete=models.CASCADE, blank=True, null=True
    )
    recurring = models.BooleanField(default=False)
    entry_price = models.CharField(max_length=100,blank=True, null=True)
    discount = models.CharField(max_length=100,blank=True, null=True)
    cover_charge = models.CharField(max_length=100,blank=True, null=True)
    no_of_people = models.CharField(max_length=100,blank=True, null=True)



class Party(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    party_name = models.CharField(max_length=100,blank=True, null=True)
    artist = models.ForeignKey(
        UserAtrist, on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    terms_conditions = models.ManyToManyField(DealTermsAndConditions, blank=True)
    rsvp = models.BooleanField(default=False)
    entry_charge = models.CharField(max_length=100,blank=True, null=True)
    cover_charge = models.CharField(max_length=100,blank=True, null=True)
    image = models.ManyToManyField(
        FileRepo, blank=True, related_name="image"
    )