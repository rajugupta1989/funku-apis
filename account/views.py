# Create your views here.

import email
import math
from datetime import datetime, timedelta
import random
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
from django.conf import settings
from django.core.mail import send_mail
import pytz









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
                                email=mobile + "@demo.com",
                                password=mobile,
                                page_count=0
                                
                            )
                        kwargs = CommonHelper.email_or_mobile(mobile)
                        credentials = {"password": mobile}
                        credentials.update(**kwargs)
                        user = authenticate(**credentials)
                        if user_data is None:
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


def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


class SendOtpOnMailAPIView(generics.CreateAPIView):
    """
    send otp on the mail
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            email = self.request.data.get("email", None)
            email_check = User.objects.filter(~Q(id=user.id), email=email,is_emailVerify=1).last()
            if email_check is not None:
                return Response(
                    {"status": False, "message": "Email already exist with emailVerified"},
                    status=status.HTTP_200_OK,
                )
            user_data = self.queryset.get(id=user.id)
            current_time = datetime.now()
            future_time = current_time + timedelta(minutes=5)
            future_time1 = future_time.replace(tzinfo=pytz.utc)
            otp = generateOTP()
            subject = 'OTP Verification Funku'
            message = 'Hi,\r\n Please enter the below mentioned OTP for email verified. \r\n '+ str(otp)
            recepient = email
            mail_response = send_mail(subject, 
                message, settings.EMAIL_HOST_USER, [recepient], fail_silently = False)
            if mail_response:
                user_data.email = email
                user_data.email_otp_valid = future_time1
                user_data.email_otp = otp
                user_data.save()    
                return Response(
                    {"status": True, "message": "OTP has been sent to your email address. Please check your mail"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": False, "message": "Please try again."}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)




class MailOtpVerifiedAPIView(generics.CreateAPIView):
    """
    otp verified the mail
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            email = self.request.data.get("email", None)
            otp = self.request.data.get("otp", None)
            email_check = User.objects.filter(~Q(id=user.id), email=email,is_emailVerify=1).last()
            if email_check is not None:
                return Response(
                    {"status": False, "message": "Email already exist with emailVerified"},
                    status=status.HTTP_200_OK,
                )
            user_data = self.queryset.filter(id=user.id,email=email).last()
            if user_data is None:
                return Response(
                    {"status": False, "message": "Email is incorrect"}, status=status.HTTP_200_OK
                )
            current_time = datetime.now()
            current_time1 = current_time.replace(tzinfo=pytz.utc)
            old_date_time = user_data.email_otp_valid
            old_date_time1 = old_date_time.replace(tzinfo=pytz.utc)
            if current_time1 >= old_date_time1:
                return Response(
                    {"status": False, "message": "OTP expired."}, status=status.HTTP_200_OK
                )
            if otp != user_data.email_otp:
                return Response(
                    {"status": False, "message": "OTP is incorrect. please try again"}, status=status.HTTP_200_OK
                )
            user_data.is_emailVerify = 1
            user_data.save()    
            return Response(
                {"status": True, "message": "Email verified"},
                status=status.HTTP_200_OK,
            )
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
            data1 = self.request.data.getlist('file')
            bulk_data = list()
            file_type = self.request.data.get("file_type", None)
            if file_type is None:
                file_type = "others"
            for f in data1:
                temp = dict()
                temp['file'] = f
                temp["title"] = self.request.data.get("title", None)
                temp["description"] = self.request.data.get("description", None)
                temp["file_type"] = file_type
                temp["created_by"] = self.request.user.id
                bulk_data.append(temp)
            serializer = self.serializer_class(data=bulk_data,many=True)
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

class UserListByIdAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.query_params.get("user_id", None)
            user = self.queryset.filter(id__in=list(eval(user_id)),is_superuser=False,is_active=True)
            serializer = self.serializer_class(instance=user,many=True)
            response = {
                    'status': True,'results': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            error = {'status': False,
                     'message': "Something Went Wrong", "error": str(e)}
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
        


class UserRoleChangeAPIView(generics.UpdateAPIView):
    """
    Update role
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def patch(self, request, *args, **kwargs):
        try:
            role = self.request.data.get("role", None)
            user_data = User.objects.get(id=kwargs["pk"])
            if user_data is not None:
                if 1 not in role:
                    default_role = [1]
                    role = default_role + role
                user_data.role.set(role)
                user_data.save()
                return Response(
                    {"status": True, "message": "Successfully role changed"}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"status": False, "message": "User does not exist"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)




class ILikeToMeetAPIView(generics.UpdateAPIView):
    """
    I like to meet
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            gender = self.request.data.get("gender",None)
            user_data = userProfileDetail.objects.get(user=user)
            if user_data is not None:
                user_data.gender_like_to_meet.set(gender)
                user_data.save()
                return Response(
                    {"status": True, "message": "Successfully  updated"}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"status": False, "message": "User does not exist"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)
        


class ILikeToFindUserForAPIView(generics.UpdateAPIView):
    """
    I like to find user for
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = userProfileDetail.objects.all()
    serializer_class = userProfileDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_find_for = self.request.data.get("user_find_for",None)
            user_data = userProfileDetail.objects.get(user=user)
            if user_data is not None:
                user_data.profile_matching_for.set(user_find_for)
                user_data.save()
                return Response(
                    {"status": True, "message": "Successfully  updated"}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"status": False, "message": "User does not exist"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(str(e))
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)