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


class UserPropertyThumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPropertyThumb
        fields = "__all__"


class UserPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProperty
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        payment = instance.payment.all().values("id", "name")
        available = PropertyAvailableFacilities.objects.filter(property=instance).last()
        available_facilities = PropertyAvailableFacilitiesSerializer(instance=available).data
        social = PropertySocialDetail.objects.filter(property=instance).last()
        social_data = PropertySocialDetailSerializer(instance=social).data
        serializer.update(
            {
                "payment": payment,
                "available_facilities":available_facilities,
                "social_data":social_data
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


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = "__all__"