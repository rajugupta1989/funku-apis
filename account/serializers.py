from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework import status
from django.utils.text import gettext_lazy as _

from common.core.validators import validate_user
from account.models import User, Role, userProfile,userProfileDetail,FileRepo
from master.serializers import genderSerializer


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"



class UserCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('mobile', 'email')


class UserVerifySerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField(required=True)
    email = serializers.CharField()
    mobile = serializers.CharField()

    class Meta:
        model = User
        fields = ('email','mobile', 'otp',)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'mobile', 'email', 'is_active', 'is_superuser')


class UserLoginSerializer(serializers.ModelSerializer):
    device = serializers.CharField(help_text=_("Email Or Mobile"), validators=[validate_user], required=True)
    password = serializers.CharField(help_text=_("Password"), max_length=128, min_length=8, required=True,
                                     write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('device', 'password',)



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    profile_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'role','email','mobile','page_count','profile','profile_detail')

    def get_profile(self, instance):
        profile_ins = userProfile.objects.filter(user=instance.id).last()
        return userProfileSerializer(instance=profile_ins).data
    def get_profile_detail(self, instance):
        profile_ins = userProfileDetail.objects.filter(user=instance.id).last()
        return userProfileDetailSerializer(instance=profile_ins).data
    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        role = instance.role.all().values("id", "name")
        serializer.update({
            "role": role
        })
        return serializer
    


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = "__all__"


class userProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfileDetail
        fields = "__all__"


    def to_representation(self, instance):
        serializer = super().to_representation(instance)
        music = instance.music.all().values("id", "name","image")
        drink = instance.drink.all().values("id", "name","image")
        bar = instance.bar.all().values("id", "name","image")
        gender = genderSerializer(instance.gender).data
        profile_matching_for = instance.profile_matching_for.all().values("id","name")
        gender_like_to_meet = instance.gender_like_to_meet.all().values("id","name")
        serializer.update({
            "music": music,
            "drink": drink,
            "bar": bar,
            "gender":gender,
            "gender_like_to_meet":gender_like_to_meet,
            "profile_matching_for":profile_matching_for
        })
        return serializer



class FileRepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileRepo
        fields = "__all__"