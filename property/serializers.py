from rest_framework import serializers
from property.models import (
    UserPropertyThumb,
    UserProperty,
    PropertyAvailableFacilities,
    PropertySocialDetail,
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
        serializer.update(
            {
                "payment": payment,
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
