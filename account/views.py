# Create your views here.

import email
from re import T
import uuid
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.text import gettext_lazy as _

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
import json
from common.helper import CommonHelper, gen_pass
from common.otp import user_activate, Update_page_count
from django.contrib.auth.password_validation import validate_password
from account.serializers import (
    UserCreateSerializer,
    UserVerifySerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    RoleSerializer,
    userProfileSerializer,
    userProfileDetailSerializer,
    FileRepoSerializer,
    UserSerializer,
)
from account.models import User, Role, userProfile, userProfileDetail,FileRepo
from account.utils import sent_sms, otp_verify
from rest_framework import serializers
from account import models
from django.db.models import Q









class RefreshToken(JSONWebTokenAPIView):
    serializer_class = RefreshJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Method to refresh the token. Token refresh only valid till original token not expired
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super(RefreshToken, self).post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(CommonHelper.render(True, response.data, "success", response.status_code))
        return Response(CommonHelper.render(False, None, response.data["non_field_errors"], response.status_code))


class RoleAPIView(generics.RetrieveAPIView):
    """
    Get all role
    """

    permission_classes = (permissions.AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            response = self.serializer_class(instance=queryset, many=True)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class Send_OtpAPIView(generics.CreateAPIView):
    """
    Account Register with mobile or email
    """

    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Method used for user registration with mobile or email
        :param request: using this parameter user get email or mobile no
        :param args: None
        :param kwargs: None
        :return:True: Success
                False: Failed
        """
        try:
            mobile = self.request.data.get("mobile", None)
            email = self.request.data.get("email", None)
            if mobile is not None:
                result = sent_sms(mobile)
                if result.status_code == 200:
                    data = json.loads(result.content.decode("utf-8"))
                    if data["Status"] == "Success":
                        response = {
                            "status": True,
                            "message": "OTP sent successfully",
                            "session_id": data["Details"],
                        }
                    else:
                        response = {"status": False, "message": data["Details"]}
                else:
                    response = {"status": False, "message": "Please try again"}
            elif email is not None:
                pass
            else:
                response = {"status": False, "message": "Send email or mobile"}
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class Verify(generics.CreateAPIView):
    """
    Verify Registred email or mobile with otp
    mobile otp only verify mobile so user can only login with mobile
    email otp only verify email so user can only login with email
    """

    model = models.User
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserVerifySerializer

    def post(self, request, *args, **kwargs):
        """
        Verify Registered email or mobile with otp
        mobile otp only verify mobile
        email otp only verify email
        :param request: using this parameter user get email or mobile no.
        :param args: None
        :param kwargs: None
        :return:True: Success
                False: Failed
        """
        try:
            mobile = self.request.data.get("mobile", None)
            session_id = self.request.data.get("session_id", None)
            email = self.request.data.get("email", None)
            otp = self.request.data.get("otp", None)
            if mobile is not None and session_id is not None:
                result = otp_verify(mobile, otp, session_id)
                if result.status_code == 200:
                    data = json.loads(result.content.decode("utf-8"))
                    if data["Status"] == "Success":
                        user_data = User.objects.filter(mobile=mobile).last()
                        if user_data is None:
                            self.model.objects.create_user(
                                mobile=mobile,
                                email=mobile + "@test.com",
                                password=mobile,
                                page_count=0
                                
                            )
                        kwargs = CommonHelper.email_or_mobile(mobile)
                        credentials = {"password": mobile}
                        credentials.update(**kwargs)
                        user = authenticate(**credentials)
                        user.role.set(['1'])
                        tokendata = {
                            "token": user.token,
                            "page_count": user.page_count,
                        }
                        response = {
                            "status": True,
                            "message": "OTP verify successfully",
                            "results": tokendata,
                        }
                    else:
                        response = {"status": False,"message":"Token expired", "error": data["Details"]}
                else:
                    response = {"status": False, "message": "OTP expired"}
            elif email is not None:
                pass
            else:
                response = {"status": False, "message": "Send email or mobile with otp"}
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            email = self.request.data.get("email", None)
            email_check = User.objects.filter(~Q(id=user.id), email=email).last()
            if email_check is not None:
                return Response(
                    {"status": False, "message": "Email already exist."},
                    status=status.HTTP_200_OK,
                )

            profile = self.queryset.get(id=user.id)
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user.id
            queryset = self.queryset.get(id=user)
            response = UserProfileUpdateSerializer(instance=queryset)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error":str(e)}
            return Response(error, status=status.HTTP_200_OK)


class ProfileImageAPIView(generics.CreateAPIView):
    """
    profile
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            page_count = self.request.data.get("page_count", None)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class ProfileImageUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile image
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            profile = self.queryset.filter(user=user.id).last()
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id).last()
            response = userProfileSerializer(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class ProfileDetailAPIView(generics.CreateAPIView):
    """
    profile detail
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            page_count = self.request.data.get("page_count", None)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class ProfileDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile detail
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            page_count = self.request.data.get("page_count", None)
            profile = self.queryset.filter(user=user.id).last()
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                if page_count is not None:
                    Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id).last()
            response = userProfileDetailSerializer(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)



class userMusicTypeAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile music
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            page_count = self.request.data.get("page_count", None)
            request.data["user"] = user.id
            profile = self.queryset.filter(user=user.id).last()
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                if page_count is not None:
                    Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id).last()
            response = userProfileDetailSerializer(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class userDrinkTypeAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile drink
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            page_count = self.request.data.get("page_count", None)
            request.data["user"] = user.id
            profile = self.queryset.filter(user=user.id).last()
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                if page_count is not None:
                    Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id).last()
            response = userProfileDetailSerializer(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)



class userBarTypeAPIView(generics.RetrieveUpdateAPIView):
    """
    Update profile bar
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            page_count = self.request.data.get("page_count", None)
            request.data["user"] = user.id
            profile = self.queryset.filter(user=user.id).last()
            serializer = self.serializer_class(instance=profile, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                if page_count is not None:
                    Update_page_count(user, page_count)
                return Response(
                    {"status": True, "results": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id).last()
            response = userProfileDetailSerializer(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class FilesRepoAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = FileRepo.objects.all()
    serializer_class = FileRepoSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': True, 'message': "Successfully created", 'results': serializer.data}
            else:
                response = {'status': False, 'message': serializer.errors}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            error = {'status': False,
                     'message': "Something Went Wrong", "error": str(e)}
            return Response(error, status=status.HTTP_200_OK)


class FileRepoAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = FileRepo.objects.all()
    serializer_class = FileRepoSerializer

    def patch(self, request, *args, **kwargs):
        try:
            fileRepo = FileRepo.objects.get(id=kwargs["pk"])
            if fileRepo is not None:
                serializer = self.serializer_class(
                    instance=fileRepo, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        'status': True, 'message': "Successfully updated", 'results': serializer.data}
                else:
                    response = {'status': False, 'message': serializer.errors}
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {'status': False,
                     'message': "Something Went Wrong", "error": str(e)}
            return Response(error, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            fileRepo = FileRepo.objects.get(id=kwargs["pk"])
            if fileRepo is not None:
                fileRepo.delete()
                response = {'status': True, 'message': "Deleted Successfully"}
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {'status': False, 'message': "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class UserSearchAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            mobile = self.request.query_params.get("mobile", None)
            user = self.queryset.filter(mobile__icontains=mobile,is_superuser=False,is_active=True)
            serializer = self.serializer_class(instance=user,many=True)
            response = {
                    'status': True,'results': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            error = {'status': False,
                     'message': "Something Went Wrong", "error": str(e)}
            return Response(error, status=status.HTTP_200_OK)