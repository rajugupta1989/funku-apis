from rest_framework import serializers
from property.models import (
    UserPropertyThumb,
    UserProperty,
    PropertyAvailableFacilities,
    PropertySocialDetail,
    FlashDealDetail,
    Deal,
    Party,
)
from master.serializers import CountrySerializer,StateSerializer,CitySerializer,DealTypeSerializer,FlashDealForSerializer,EntryTypeSerializer,BrandTypeSerializer,drink_typeSerializer
from account.serializers import UserProfileUpdateSerializer


class UserPropertyThumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPropertyThumb
        fields = "__all__"


class UserPropertySerializer(serializers.ModelSerializer):
    propertythumb = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProperty
        fields = "__all__"

    def get_propertythumb(self, instance):
        pro_ins = UserPropertyThumb.objects.filter(property=instance.id).last()
        return UserPropertyThumbSerializer(instance=pro_ins).data

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        payment = instance.payment.all().values("id", "name")
        available = PropertyAvailableFacilities.objects.filter(property=instance).last()
        available_facilities = PropertyAvailableFacilitiesSerializer(instance=available).data
        social = PropertySocialDetail.objects.filter(property=instance).last()
        social_data = PropertySocialDetailSerializer(instance=social).data
        manager = UserProfileUpdateSerializer(instance=instance.manager,many=True).data
        country = CountrySerializer(instance=instance.country).data
        state = StateSerializer(instance=instance.state).data
        city = CitySerializer(instance=instance.city).data
        serializer.update(
            {
                "payment": payment,
                "available_facilities":available_facilities,
                "social_data":social_data,
                "manager":manager,
                "country":country,
                "state":state,
                "city":city


            }
        )
        return serializer


class PropertyAvailableFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAvailableFacilities
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        facilities = instance.facilities.all().values(
            "id", "name", "description", "image"
        )
        serializer.update(
            {
                "facilities": facilities,
            }
        )
        return serializer


class PropertySocialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertySocialDetail
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        exterior_gallery = instance.exterior_gallery.all().values("id", "title","description","file")
        interior_gallery = instance.interior_gallery.all().values("id", "title","description","file")
        menu_place = instance.menu_place.all().values("id", "title","description","file")
        promoter = instance.promoter.all().values("id", "email","first_name","last_name")
        serializer.update({
            "exterior_gallery": exterior_gallery,
            "interior_gallery": interior_gallery,
            "menu_place": menu_place,
            "promoter": promoter,
        })
        return serializer


class FlashDealDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashDealDetail
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        terms_conditions = instance.terms_conditions.all().values("id", "name")
        property_ = UserPropertySerializer(instance=instance.property).data
        category = drink_typeSerializer(instance=instance.category).data
        deal_for = FlashDealForSerializer(instance=instance.deal_for).data
        brand = BrandTypeSerializer(instance=instance.brand).data
        serializer.update({
            "property": property_,
            "category": category,
            "deal_for": deal_for,
            "brand": brand,
            "terms_conditions":terms_conditions
        })
        return serializer

class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        terms_conditions = instance.terms_conditions.all().values("id", "name")
        property_ = UserPropertySerializer(instance=instance.property).data
        deal_type = DealTypeSerializer(instance=instance.deal_type).data
        deal_for = FlashDealForSerializer(instance=instance.deal_for).data
        entry_type = EntryTypeSerializer(instance=instance.entry_type).data
        serializer.update({
            "property": property_,
            "deal_type": deal_type,
            "deal_for": deal_for,
            "entry_type": entry_type,
            "terms_conditions":terms_conditions
        })
        return serializer


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        terms_conditions = instance.terms_conditions.all().values("id", "name")
        image = instance.image.all().values("id", "title","description","file")
        property_ = UserPropertySerializer(instance=instance.property).data
        serializer.update({
            "property": property_,
            "terms_conditions":terms_conditions,
            "image":image
        })
        return serializer
