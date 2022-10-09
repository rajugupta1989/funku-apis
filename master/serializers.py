from rest_framework import serializers
from master.models import (
    bar_type,
    masterAvatarProfile,
    gender,
    music_type,
    drink_type,
    property_type,
    Country,
    State,
    City,
    PaymentMethod,
    PropertyFacilities,
    ArtistType,
    Language,
    AdditionalFeature
)


class masterAvatarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = masterAvatarProfile
        fields = "__all__"


class genderSerializer(serializers.ModelSerializer):
    class Meta:
        model = gender
        fields = "__all__"


class music_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = music_type
        fields = "__all__"


class drink_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = drink_type
        fields = "__all__"


class bar_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = bar_type
        fields = "__all__"


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = property_type
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    state = serializers.ListField(required=False)

    class Meta:
        model = Country
        fields = "__all__"

class StateSerializer(serializers.ModelSerializer):
    city = serializers.ListField(required=False)

    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

class PropertyFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFacilities
        fields = "__all__"

class ArtistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistType
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class AdditionalFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFeature
        fields = "__all__"