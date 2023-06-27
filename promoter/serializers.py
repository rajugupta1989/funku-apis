from rest_framework import serializers
from account.models import FileRepo
from promoter.models import (
   UserPromoter,
   PromoterSocialProfile
)


class UserPromoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPromoter
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        payment = instance.payment.all().values("id", "name")
        profile_image = FileRepo.objects.get(id=instance.profile_image_id)
        serializer.update(
            {
                "payment": payment,
                "profile_image_path":str(profile_image.file)
            }
        )
        return serializer



class PromoterSocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoterSocialProfile
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        promoter_gallery = instance.promoter_gallery.all().values("id", "file")
        promoter_additional_feature = instance.promoter_additional_feature.all().values("id", "name")
        serializer.update(
            {
                "promoter_gallery": promoter_gallery,
                "promoter_additional_feature":promoter_additional_feature,
            }
        )
        return serializer