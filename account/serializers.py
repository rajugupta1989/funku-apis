from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework import status
from django.utils.text import gettext_lazy as _

from common.core.validators import validate_user
from account.models import User, Role, userProfile,userProfileDetail,FileRepo



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

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'role','email','mobile','page_count')





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
        serializer.update({
            "music": music,
            "drink": drink,
            "bar": bar
        })
        return serializer



class FileRepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileRepo
        fields = "__all__"