from rest_framework import serializers
from account.models import FileRepo, User
from master.models import PropertyFacilities, music_type
from property.models import (
    UserBooking,
    UserPropertyThumb,
    UserProperty,
    PropertyAvailableFacilities,
    PropertySocialDetail,
    FlashDealDetail,
    Deal,
    Party,
    UserEnquiry,
    UserEnquiryStatus,
)
from master.serializers import PropertyFacilitiesSerializer, PropertyTypeSerializer,OccasionSerializer,CountrySerializer,StateSerializer,CitySerializer,DealTypeSerializer,FlashDealForSerializer,EntryTypeSerializer,BrandTypeSerializer,drink_typeSerializer, music_typeSerializer
from account.serializers import FileRepoSerializer, UserProfileUpdateSerializer, userProfileDetailSerializer


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
        documents_verified_by = UserProfileUpdateSerializer(instance=instance.documents_verified_by).data
        country = CountrySerializer(instance=instance.country).data
        state = StateSerializer(instance=instance.state).data
        city = CitySerializer(instance=instance.city).data
        property_type = PropertyTypeSerializer(instance=instance.property_type).data
        documents_file = FileRepo.objects.filter(id__in=instance.documents.all())
        documents = FileRepoSerializer(documents_file, many=True).data
        serializer.update(
            {
                "payment": payment,
                "available_facilities":available_facilities,
                "social_data":social_data,
                "manager":manager,
                "country":country,
                "state":state,
                "city":city,
                "documents_verified_by":documents_verified_by,
                "property_type":property_type,
                "documents":documents,


            }
        )
        return serializer


class PropertyAvailableFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAvailableFacilities
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        facility = PropertyFacilities.objects.filter(id__in=instance.facilities.all())
        facilities = PropertyFacilitiesSerializer(facility, many=True).data
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
        exterior = FileRepo.objects.filter(id__in=instance.exterior_gallery.all())
        interior = FileRepo.objects.filter(id__in=instance.interior_gallery.all())
        video = FileRepo.objects.filter(id__in=instance.video_file.all())
        video_file = FileRepoSerializer(video, many=True).data
        menu = FileRepo.objects.filter(id__in=instance.menu_place.all())
        exterior_gallery = FileRepoSerializer(exterior, many=True).data
        interior_gallery = FileRepoSerializer(interior, many=True).data
        menu_place = FileRepoSerializer(menu, many=True).data
        promoter = instance.promoter.all().values("id", "email","first_name","last_name")
        serializer.update({
            "exterior_gallery": exterior_gallery,
            "interior_gallery": interior_gallery,
            "video_file":video_file,
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
        video = FileRepo.objects.filter(id__in=instance.flash_deal_video_file.all())
        flash_deal_video_file = FileRepoSerializer(video, many=True).data
        deal_type = DealTypeSerializer(instance=instance.deal_type.all(),many=True).data
        deal_for = FlashDealForSerializer(instance=instance.deal_for.all(),many=True).data
        music_type = music_typeSerializer(instance=instance.music_type.all(),many=True).data
        entry_type = EntryTypeSerializer(instance=instance.entry_type.all(),many=True).data
        drink_type = drink_typeSerializer(instance=instance.drink_type.all(),many=True).data
        brand_type = BrandTypeSerializer(instance=instance.brand_type.all(),many=True).data

        serializer.update({
            "property": property_,
            "flash_deal_video_file":flash_deal_video_file,
            "drink_type": drink_type,
            "deal_for": deal_for,
            "deal_type":deal_type,
            "music_type":music_type,
            "brand_type": brand_type,
            "entry_type":entry_type,
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
        video = FileRepo.objects.filter(id__in=instance.deal_video_file.all())
        deal_video_file = FileRepoSerializer(video, many=True).data
        deal_type = DealTypeSerializer(instance=instance.deal_type.all(),many=True).data
        deal_for = FlashDealForSerializer(instance=instance.deal_for.all(),many=True).data
        music_type = music_typeSerializer(instance=instance.music_type.all(),many=True).data
        entry_type = EntryTypeSerializer(instance=instance.entry_type.all(),many=True).data
        drink_type = drink_typeSerializer(instance=instance.drink_type.all(),many=True).data
        brand_type = BrandTypeSerializer(instance=instance.brand_type.all(),many=True).data
        serializer.update({
            "property": property_,
            "deal_type": deal_type,
            "deal_video_file":deal_video_file,
            "deal_for": deal_for,
            "entry_type": entry_type,
            "music_type":music_type,
            "drink_type":drink_type,
            "brand_type":brand_type,
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
        image = FileRepo.objects.filter(id__in=instance.image.all())
        image_serializer = FileRepoSerializer(image, many=True).data
        video = FileRepo.objects.filter(id__in=instance.party_video_file.all())
        party_video_file = FileRepoSerializer(video, many=True).data
        property_ = UserPropertySerializer(instance=instance.property).data
        deal_type = DealTypeSerializer(instance=instance.deal_type.all(),many=True).data
        deal_for = FlashDealForSerializer(instance=instance.deal_for.all(),many=True).data
        music_type = music_typeSerializer(instance=instance.music_type.all(),many=True).data
        entry_type = EntryTypeSerializer(instance=instance.entry_type.all(),many=True).data
        drink_type = drink_typeSerializer(instance=instance.drink_type.all(),many=True).data
        brand_type = BrandTypeSerializer(instance=instance.brand_type.all(),many=True).data

        serializer.update({
            "property": property_,
            "terms_conditions":terms_conditions,
            "image":image_serializer,
            "party_video_file":party_video_file,
            "entry_type":entry_type,
            "music_type":music_type,
            "drink_type":drink_type,
            "brand_type":brand_type,
            "deal_for":deal_for,
            "deal_type":deal_type
        })
        return serializer

class UserEnquiryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnquiryStatus
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        property_ = UserPropertySerializer(instance=instance.user_property).data
        serializer.update({
            "user_property": property_
        })
        return serializer


class UserEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnquiry
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        type_of_place = PropertyTypeSerializer(instance.type_of_place,many=True).data
        occasion = OccasionSerializer(instance.occasion).data
        specific_club = UserPropertySerializer(instance.specific_club.all(), many=True).data
        enquiry_obj= UserEnquiryStatus.objects.filter(user_enquiry=instance)
        enquiry_status = UserEnquiryStatusSerializer(enquiry_obj,many=True).data
        serializer.update({
            "occasion": occasion,
            "type_of_place":type_of_place,
            "specific_club":specific_club,
            "enquiry_status":enquiry_status
        })
        return serializer




class UserEnquiryForOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnquiry
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        type_of_place = PropertyTypeSerializer(instance.type_of_place,many=True).data
        occasion = OccasionSerializer(instance.occasion).data
        enquiry_obj= UserEnquiryStatus.objects.filter(user_enquiry=instance)
        enquiry_status = UserEnquiryStatusSerializer(enquiry_obj,many=True).data
        user_ins = User.objects.get(id=instance.user.id)
        user_data = UserProfileUpdateSerializer(user_ins).data
        serializer.update({
            "user": user_data,
            "occasion": occasion,
            "type_of_place":type_of_place,
            "enquiry_status":enquiry_status
        })
        return serializer
    

class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBooking
        fields = "__all__"

    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        user_ins = User.objects.get(id=instance.user.id)
        user_data = UserProfileUpdateSerializer(user_ins).data
        property_ = UserPropertySerializer(instance=instance.property).data
        if instance.deal:
            deal = DealSerializer(instance.deal).data
        else:
            deal = None
        if instance.flash_deal:
            flash_deal = FlashDealDetailSerializer(instance.flash_deal).data
        else:
            flash_deal = None
        if instance.party:
            party = PartySerializer(instance.party).data
        else:
            party = None

        serializer.update({
            "user": user_data,
            "property": property_,
            "deal": deal,
            "flash_deal":flash_deal,
            "party":party
        })
        return serializer