from django.db import models
from common.abstract_model import CommonAbstractModel
# Create your models here.


class masterAvatarProfile(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    profile_image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)



class gender(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)



class music_type(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)



class drink_type(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)


class bar_type(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)



class property_type(CommonAbstractModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    def __str__(self):
        return "{}".format(self.name)



class Country(CommonAbstractModel):

    code = models.CharField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class State(CommonAbstractModel):
    country = models.ForeignKey(Country,on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class City(CommonAbstractModel):
    country = models.ForeignKey(Country,on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)



class PaymentMethod(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class PropertyFacilities(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    description = models.CharField(max_length=300,blank=True,null=True)
    image = models.FileField(upload_to="documents", null=True, default=None)
    def __str__(self):
        return "{}".format(self.name)


class ArtistType(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

class Language(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

class AdditionalFeature(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class DealTermsAndConditions(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)



class FlashDealFor(CommonAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

class BrandType(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    
    def __str__(self):
        return "{}".format(self.name)
    
class DealType(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    
    def __str__(self):
        return "{}".format(self.name)

class EntryType(CommonAbstractModel):
    name = models.CharField(max_length=30,blank=True,null=True)
    
    def __str__(self):
        return "{}".format(self.name)