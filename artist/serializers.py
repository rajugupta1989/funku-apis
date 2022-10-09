from rest_framework import serializers
from account.models import FileRepo
from artist.models import (
   UserAtrist,
   AtristSocialProfile
)


class UserAtristSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAtrist
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        payment = instance.payment.all().values("id", "name")
        language = instance.language.all().values("id", "name")
        artist_type = instance.artist_type.all().values("id", "name")
        profile_image = FileRepo.objects.get(id=instance.profile_image_id)
        serializer.update(
            {
                "payment": payment,
                "language":language,
                "artist_type":artist_type,
                "profile_image_path":str(profile_image.file)
            }
        )
        return serializer



class AtristSocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtristSocialProfile
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        gallery = instance.gallery.all().values("id", "file")
        additional_feature = instance.additional_feature.all().values("id", "name")
        serializer.update(
            {
                "gallery": gallery,
                "additional_feature":additional_feature,
            }
        )
        return serializer