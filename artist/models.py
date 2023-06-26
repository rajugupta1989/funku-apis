from django.db import models
from common.abstract_model import CommonAbstractModel
from account.models import User, FileRepo
from master.models import (
    bar_type,
    drink_type,
    gender,
    music_type,
    ArtistType,
    Language,
    AdditionalFeature,
)
from master.models import Country, State, City, PaymentMethod, PropertyFacilities,AdditionalFeature


class UserAtrist(CommonAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    profile_image = models.ForeignKey(FileRepo, on_delete=models.CASCADE, blank=True, null=True)
    artist_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.ForeignKey(gender, on_delete=models.CASCADE, blank=True, null=True)
    artist_type = models.ManyToManyField(ArtistType, blank=True, null=True)
    language = models.ManyToManyField(Language, blank=True, null=True)
    about = models.CharField(max_length=300, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True
    )
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    charges = models.CharField(max_length=100, blank=True, null=True)
    payment = models.ManyToManyField(PaymentMethod, blank=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)


class AtristSocialProfile(CommonAbstractModel):
    artist = models.ForeignKey(UserAtrist, on_delete=models.CASCADE, unique=True)
    gallery = models.ManyToManyField(FileRepo, blank=True, related_name="gallery") 
    image_instagram = models.CharField(max_length=250, blank=True, null=True)
    image_facebook = models.CharField(max_length=250, blank=True, null=True) 
    instagram = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    additional_feature = models.ManyToManyField(AdditionalFeature, blank=True, related_name="additional_feature")
    business_contact_no = models.CharField(max_length=100, blank=True, null=True)
    business_email = models.CharField(max_length=100, blank=True, null=True)