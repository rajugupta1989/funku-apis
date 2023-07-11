import math
import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.text import gettext_lazy as _
from rest_framework import generics, exceptions, pagination, status
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.db import transaction, IntegrityError
from property.lat_long_calculator import generate_qr_code, get_lat_long_calculated
import json
from django.db.models import Q
import datetime
import base64
import uuid
from property.models import *
from property.serializers import *
from django.conf import settings
from django.core.mail import send_mail
import pytz
from django.contrib.postgres.search import SearchVector
from itertools import chain
from datetime import date

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from property.filters import DealFilter

# Create your views here.


class PropertyProfileImageAPIView(generics.CreateAPIView):
    """
    property profile image
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserPropertyThumb.objects.all()
    serializer_class = UserPropertyThumbSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
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


class PropertyProfileImageUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Property Update profile image
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserPropertyThumb.objects.all()
    serializer_class = UserPropertyThumbSerializer

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
            response = self.serializer_class(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class AddPropertyAPIView(generics.ListCreateAPIView):
    """
    Add property
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            ###############################
            recepient = self.request.data.get("email", None)
            property_code = self.request.data.get("property_code", None)
            if recepient is not None and (
                property_code is not None or property_code != ""
            ):
                chech_data = UserPropertyMailVerified.objects.filter(
                    user_id=user.id, email=recepient, property_code=property_code
                ).last()
            if chech_data is None:
                return Response(
                    {
                        "status": False,
                        "message": "Email or property code is incorrect, please verify the email and generate a new property code",
                    },
                    status=status.HTTP_200_OK,
                )
            request.data["is_emailVerify"] = 1
            #############################
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                UserPropertyMailVerified.objects.filter(
                    user_id=user.id, email=recepient, property_code=property_code
                ).delete()
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
            profile = self.queryset.filter(user=user.id)
            page = self.paginate_queryset(profile)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class PropertyVerifyAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer

    def post(self, request, *args, **kwargs):
        try:
            property_id = self.request.data.get("property_id",None)
            property_status = self.request.data.get("property_status",None)
            
            if property_id is not None and property_status is not None:
                data = UserProperty.objects.get(id=property_id)
                if data is not None:
                    data.documents_verified_by_id = self.request.user.id
                    data.documents_verified_date = date.today()
                    data.document_ferified = property_status
                    data.save()
                    if property_status:
                        mess = "property successfully verified"
                    else:
                        mess = "property successfully unverified"
                    return Response(
                        {
                            "status": True,
                            "message": mess,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "status": False,
                            "message": "Property id doed not exist",
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                        {
                            "status": False,
                            "message": "Property id and property status required",
                        },
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


class AddPropertyWebAPIView(generics.ListCreateAPIView):
    """
    Add property web
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer
    serializer_class_thumb = UserPropertyThumbSerializer
    serializer_class_facility = PropertyAvailableFacilitiesSerializer
    serializer_class_social = PropertySocialDetailSerializer

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user = self.request.user
                request.data["user"] = user.id
                ###############################
                recepient = self.request.data.get("email", None)
                property_code = self.request.data.get("property_code", None)
                if recepient is not None and (
                    property_code is not None or property_code != ""
                ):
                    chech_data = UserPropertyMailVerified.objects.filter(
                        user_id=user.id, email=recepient, property_code=property_code
                    ).last()
                if chech_data is None:
                    return Response(
                        {
                            "status": False,
                            "message": "Email or property code is incorrect, please verify the email and generate a new property code",
                        },
                        status=status.HTTP_200_OK,
                    )
                request.data["is_emailVerify"] = 1
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                    request.data["property"] = serializer.data["id"]
                    serializer_thumb = self.serializer_class_thumb(data=request.data)
                    if serializer_thumb.is_valid(raise_exception=False):
                        serializer_thumb.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_thumb.errors},
                            status=status.HTTP_200_OK,
                        )
                    serializer_facility = self.serializer_class_facility(
                        data=request.data
                    )
                    if serializer_facility.is_valid(raise_exception=False):
                        serializer_facility.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_facility.errors},
                            status=status.HTTP_200_OK,
                        )
                    serializer_social = self.serializer_class_social(data=request.data)
                    if serializer_social.is_valid(raise_exception=False):
                        serializer_social.save()
                        UserPropertyMailVerified.objects.filter(
                            user_id=user.id,
                            email=recepient,
                            property_code=property_code,
                        ).delete()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_social.errors},
                            status=status.HTTP_200_OK,
                        )

                    return Response(
                        {"status": True, "results": serializer.data},
                        status=status.HTTP_200_OK,
                    )
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer.errors},
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

    def get(self, request, *args, **kwargs):
        try:
            if "Super Admin" in list(self.request.user.role.all().values_list('name',flat=True)):
                profile = self.queryset.all()
            else:
                user = self.request.user
                profile = self.queryset.filter(user=user.id)
            response = self.serializer_class(profile, many=True)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class UpdateDeletePropertyWebAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Property Update web
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer
    serializer_class_thumb = UserPropertyThumbSerializer
    serializer_class_facility = PropertyAvailableFacilitiesSerializer
    serializer_class_social = PropertySocialDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user = self.request.user
                request.data["user"] = user.id
                profile = self.queryset.get(id=kwargs["pk"])
                serializer = self.serializer_class(instance=profile, data=request.data)
                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer.errors},
                        status=status.HTTP_200_OK,
                    )
                facility = PropertyAvailableFacilities.objects.filter(
                    property=kwargs["pk"]
                ).last()
                request.data["property"] = kwargs["pk"]
                serializer_facility = self.serializer_class_facility(
                    instance=facility, data=request.data
                )
                if serializer_facility.is_valid(raise_exception=False):
                    serializer_facility.save()
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer_facility.errors},
                        status=status.HTTP_200_OK,
                    )
                social = PropertySocialDetail.objects.filter(
                    property=kwargs["pk"]
                ).last()
                serializer_social = self.serializer_class_social(
                    instance=social, data=request.data
                )
                if serializer_social.is_valid(raise_exception=False):
                    serializer_social.save()
                    return Response(
                        {"status": True, "message": "Successfully updated"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer_social.errors},
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

    def delete(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(id=kwargs["pk"])
            profile.delete()
            response = {"status": True, "Message": "Successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(id=kwargs["pk"])
            response = self.serializer_class(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class UpdateDeletePropertyAPIView(generics.RetrieveUpdateAPIView):
    """
    Property Update
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            profile = self.queryset.get(id=kwargs["pk"])
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
            profile = self.queryset.get(id=kwargs["pk"])
            response = self.serializer_class(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)


class AddPropertySocialAPIView(generics.CreateAPIView):
    """
    Add property Social
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PropertySocialDetail.objects.all()
    serializer_class = PropertySocialDetailSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
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


class UpdatePropertySocialAPIView(generics.RetrieveUpdateAPIView):
    """
    Social Property Update
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PropertySocialDetail.objects.all()
    serializer_class = PropertySocialDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            property_social = self.queryset.get(pk=kwargs["pk"])
            serializer = self.serializer_class(
                instance=property_social, data=request.data
            )
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
            property_social = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(property_social)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class AddAvailableFacilitiesAPIView(generics.CreateAPIView):
    """
    Add property available facility
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PropertyAvailableFacilities.objects.all()
    serializer_class = PropertyAvailableFacilitiesSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
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


class UpdateAvailableFacilitiesAPIView(generics.RetrieveUpdateAPIView):
    """
    Property available facility Update
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PropertyAvailableFacilities.objects.all()
    serializer_class = PropertyAvailableFacilitiesSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            property_social = self.queryset.get(pk=kwargs["pk"])
            serializer = self.serializer_class(
                instance=property_social, data=request.data
            )
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
            property_social = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(property_social)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class AddFlashDealAPIView(generics.ListCreateAPIView):
    """
    Add pflash deal
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = FlashDealDetail.objects.all()
    serializer_class = FlashDealDetailSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully created",
                        "results": serializer.data,
                    },
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
            user_id = self.request.GET.get("user_id", None)
            deal = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(deal)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


class UpdateFlashDealAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update flash deal
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = FlashDealDetail.objects.all()
    serializer_class = FlashDealDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            deal = self.queryset.get(pk=kwargs["pk"])
            serializer = self.serializer_class(instance=deal, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully Updated",
                        "results": serializer.data,
                    },
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
            deal = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(deal)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class AddDealAPIView(generics.ListCreateAPIView):
    """
    Add deal
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully created",
                        "results": serializer.data,
                    },
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
            user_id = self.request.GET.get("user_id", None)
            profile = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(profile)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


class UpdateDealAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update deal
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            deal = self.queryset.get(pk=kwargs["pk"])
            serializer = self.serializer_class(instance=deal, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully Updated",
                        "results": serializer.data,
                    },
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
            deal = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(deal)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class AddPartyAPIView(generics.ListCreateAPIView):
    """
    Add Party
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully created",
                        "results": serializer.data,
                    },
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
            user_id = self.request.GET.get("user_id", None)
            party = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(party)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


class UpdatePartyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update Party
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            deal = self.queryset.get(pk=kwargs["pk"])
            serializer = self.serializer_class(instance=deal, data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully Updated",
                        "results": serializer.data,
                    },
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
            deal = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(deal)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class GetDealByLatLongAPIView(generics.ListAPIView):
    """
    Add deal by lat long
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = DealSerializer

    def get(self, request, *args, **kwargs):
        try:
            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)
            date_range = request.query_params.get("date_range", None)
            if date_range is None or date_range == "":
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat, long, distance)
                property_id = (
                    self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                    .filter(long__gte=data.long2, long__lte=data.long1)
                    .values_list("id", flat=True)
                )
                deal_inst = Deal.objects.filter(
                    property__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                )
            else:
                date_list = date_range.split(",")
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat, long, distance)
                    property_id = (
                        self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                        .filter(long__gte=data.long2, long__lte=data.long1)
                        .values_list("id", flat=True)
                    )
                    deal_id = Deal.objects.filter(
                        property__in=property_id,
                        start_date__date__lte=current_datetime,
                        end_date__date__gte=current_datetime,
                    ).values_list("id", flat=True)
                    deal_list.append(deal_id)
                deal_inst = Deal.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class GetFlashDealByLatLongAPIView(generics.ListAPIView):
    """
    Add flash deal by lat long
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = FlashDealDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)
            date_range = request.query_params.get("date_range", None)
            if date_range is None or date_range == "":
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat, long, distance)
                property_id = (
                    self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                    .filter(long__gte=data.long2, long__lte=data.long1)
                    .values_list("id", flat=True)
                )
                deal_inst = FlashDealDetail.objects.filter(
                    property__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                )
            else:
                date_list = date_range.split(",")
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat, long, distance)
                    property_id = (
                        self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                        .filter(long__gte=data.long2, long__lte=data.long1)
                        .values_list("id", flat=True)
                    )
                    deal_id = FlashDealDetail.objects.filter(
                        property__in=property_id,
                        start_date__date__lte=current_datetime,
                        end_date__date__gte=current_datetime,
                    ).values_list("id", flat=True)
                    deal_list.append(deal_id)
                deal_inst = FlashDealDetail.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class GetPartyByLatLongAPIView(generics.ListAPIView):
    """
    Add Party by lat long
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = PartySerializer

    def get(self, request, *args, **kwargs):
        try:
            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)
            date_range = request.query_params.get("date_range", None)
            if date_range is None or date_range == "":
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat, long, distance)
                property_id = (
                    self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                    .filter(long__gte=data.long2, long__lte=data.long1)
                    .values_list("id", flat=True)
                )
                deal_inst = Party.objects.filter(
                    property__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                )
            else:
                date_list = date_range.split(",")
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat, long, distance)
                    property_id = (
                        self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                        .filter(long__gte=data.long2, long__lte=data.long1)
                        .values_list("id", flat=True)
                    )
                    deal_id = Party.objects.filter(
                        property__in=property_id,
                        start_date__date__lte=current_datetime,
                        end_date__date__gte=current_datetime,
                    ).values_list("id", flat=True)
                    deal_list.append(deal_id)
                deal_inst = Party.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class GetPropertyByLatLongAPIView(generics.ListAPIView):
    """
    Get property by lat long
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer

    def get(self, request, *args, **kwargs):
        try:
            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)
            data = get_lat_long_calculated(lat, long, distance)
            property = self.queryset.filter(
                lat__gte=data.lat1, lat__lte=data.lat2
            ).filter(long__gte=data.long2, long__lte=data.long1)
            serializers = self.serializer_class(property, many=True)
            response = {"status": True, "results": serializers.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class GetUpdateUserEnquiryAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get user enquiry and update
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserEnquiry.objects.all()
    serializer_class = UserEnquirySerializer

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.user
            party = self.queryset.get(pk=kwargs["pk"], user=user_id)
            serializer = self.serializer_class(party)
            response = {"status": True, "results": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            user_id = self.request.user
            party = self.queryset.get(pk=kwargs["pk"], user=user_id)
            party.delete()
            dict = {"status": True, "message": "Enquiry deleted Successfully"}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        try:
            user_remark = self.request.data.get("user_remark", None)
            user_enquiry_status = self.request.data.get("user_enquiry_status", None)
            user_enquiry = kwargs["pk"]
            User_enquiry = UserEnquiry.objects.get(id=user_enquiry)
            if User_enquiry is not None:
                User_enquiry.user_enquiry_status = user_enquiry_status
                User_enquiry.save()
            enquiry_status = UserEnquiryStatus.objects.filter(user_enquiry=user_enquiry)
            for data in enquiry_status:
                data.user_status = "Cancel"
                data.user_remark = user_remark
                data.save()
            return Response(
                {"status": True, "message": "Successfully cancelled"},
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


class UserEnquiryAPIView(generics.ListCreateAPIView):
    """
    User Enquiry
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserEnquiry.objects.all().order_by("-created_date")
    serializer_class = UserEnquirySerializer

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user = self.request.user
                request.data["user"] = user.id
                specific_club = self.request.data.get("specific_club", None)
                type_of_place = self.request.data.get("type_of_place", None)
                lat = self.request.data.get("lat", None)
                long = self.request.data.get("long", None)
                distance = self.request.data.get("distance", None)
                if len(specific_club) > 0:
                    serializer = self.serializer_class(data=request.data)
                elif len(type_of_place) > 0:
                    data = get_lat_long_calculated(lat, long, distance)
                    property = (
                        UserProperty.objects.filter(
                            lat__gte=data.lat1, lat__lte=data.lat2
                        )
                        .filter(
                            long__gte=data.long2,
                            long__lte=data.long1,
                            property_type__in=type_of_place,
                        )
                        .values_list("id", flat=True)
                    )
                    if len(property) > 0:
                        request.data["specific_club"] = property
                        request.data["type_of_place"] = type_of_place
                        serializer = self.serializer_class(data=request.data)
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "status": False,
                                "message": "Your selected type of place is not fund in this area to send enquiry, please increase your distance",
                            },
                            status=status.HTTP_200_OK,
                        )
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "status": False,
                            "message": "specific_club or type_of_place is required in the list",
                        },
                        status=status.HTTP_200_OK,
                    )

                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                    for enq in request.data["specific_club"]:
                        enquiry_status = UserEnquiryStatus()
                        enquiry_status.user_enquiry_id = serializer.data["id"]
                        enquiry_status.user_property_id = enq
                        enquiry_status.save()
                    return Response(
                        {
                            "status": True,
                            "message": "Successfully created",
                            "results": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                transaction.set_rollback(True)
                return Response(
                    {"status": False, "error": serializer.errors},
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

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.user
            party = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(party)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


class ClubOwnerTakeActionOnUserEnquiryAPIView(generics.RetrieveUpdateAPIView):
    """
    Club owner take action on user enquiry
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserEnquiry.objects.all().order_by("-created_date")
    serializer_class = UserEnquiryForOwnerSerializer

    def patch(self, request, *args, **kwargs):
        try:
            club_owner_remark = self.request.data.get("club_owner_remark", None)
            club_owner_status = self.request.data.get("club_owner_status", None)
            user_property = self.request.data.get("user_property", None)
            user_enquiry = self.request.data.get("user_enquiry", None)
            token_amount = self.request.data.get("token_amount", None)
            club_owner_quotation = self.request.data.get("club_owner_quotation", None)
            enquiry_status = UserEnquiryStatus.objects.filter(
                user_property=user_property, user_enquiry=user_enquiry
            ).last()
            if enquiry_status is not None:
                enquiry_status.club_owner_status = club_owner_status
                enquiry_status.club_owner_remark = club_owner_remark
                enquiry_status.token_amount = token_amount
                enquiry_status.club_owner_quotation = club_owner_quotation
                enquiry_status.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully " + str(club_owner_status),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "status": True,
                        "message": "Successfully not " + str(club_owner_status),
                    },
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

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            property = self.queryset.filter(specific_club__user=user)
            serializers = self.serializer_class(property, many=True)
            response = {"status": True, "results": serializers.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)


class UserTakeActionOnUserEnquiryAPIView(generics.RetrieveUpdateAPIView):
    """
    User take action on user enquiry
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserEnquiry.objects.all()
    serializer_class = UserEnquiryForOwnerSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user_remark = self.request.data.get("user_remark", None)
            user_status = self.request.data.get("user_status", None)
            user_property = self.request.data.get("user_property", None)
            user_enquiry = self.request.data.get("user_enquiry", None)
            enquiry_status = UserEnquiryStatus.objects.filter(
                user_property=user_property, user_enquiry=user_enquiry
            ).last()
            if enquiry_status is not None:
                enquiry_status.user_status = user_status
                enquiry_status.user_remark = user_remark
                enquiry_status.save()
                return Response(
                    {"status": True, "message": "Successfully " + str(user_status)},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": True, "message": "Successfully not " + str(user_status)},
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


class UserBookingAPIView(generics.ListCreateAPIView):
    """
    User booking
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            booking_code = "Book" + str(uuid.uuid4().int)[:4]
            request.data["booking_code"] = booking_code
            # key = Fernet.generate_key()
            # fernet = Fernet(key)
            message = str(request.data)
            encMessage = base64.b64encode(message.encode("ascii", "strict"))
            print("encMessage", encMessage)
            # decMessage = fernet.decrypt(encMessage).decode()
            # print('decMessage',decMessage)
            respon_ = generate_qr_code(encMessage)
            request.data["qr_code"] = respon_
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Successfully Booked",
                        "results": serializer.data,
                    },
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
            user_id = self.request.user
            party = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(party)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


class OwnerBookingAPIView(generics.RetrieveUpdateAPIView):
    """
    Owner booking
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            # request.data["user"] = user.id
            message = self.request.data.get("data", None)
            msg = base64.b64decode(message)
            decMessage = msg.decode("ascii", "strict")
            print("data_check", decMessage)
            dic_key = eval(decMessage)
            check_data = UserBooking.objects.filter(
                booking_code=dic_key["booking_code"], booking_status_from_owner=False
            ).last()
            if check_data is not None:
                check_data.booking_status_from_owner = True
                check_data.save()
                return Response(
                    {"status": True, "message": "Successfully done"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": False, "message": "QR code is not correct or expired"},
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

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.user
            property_id = UserProperty.objects.filter(user=user_id).values_list(
                "id", flat=True
            )
            party = self.queryset.filter(property_id__in=property_id)
            page = self.paginate_queryset(party)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False, "message": "something went wrong", "error": str(e)}
            return Response(dict, status=status.HTTP_200_OK)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class SendOtpOnMailVerifiedPropertyAPIView(generics.CreateAPIView):
    """
    send otp on the mail property
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProperty.objects.all()
    serializer_class = UserPropertySerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
            recepient = self.request.data.get("email", None)
            user_otp = self.request.data.get("user_otp", None)
            ###############################
            current_time = datetime.datetime.now()
            future_time = current_time + datetime.timedelta(minutes=5)
            future_time1 = future_time.replace(tzinfo=pytz.utc)
            otp = generateOTP()
            subject = "OTP Verification Funku"
            message = (
                "Hi,\r\n Please enter the below mentioned OTP for email verified. \r\n "
                + str(otp)
            )
            if recepient is not None and (user_otp is None or user_otp == ""):
                # mail_response = send_mail(subject,
                #     message, settings.EMAIL_HOST_USER, [recepient], fail_silently = False)
                if True:
                    chech_data = UserPropertyMailVerified.objects.filter(
                        user_id=user.id, email=recepient
                    ).last()
                    if chech_data is not None:
                        chech_data.email_otp_valid = future_time1
                        chech_data.email_otp = otp
                        chech_data.save()
                    else:
                        chech_data = UserPropertyMailVerified()
                        chech_data.user_id = user.id
                        chech_data.email = recepient
                        chech_data.email_otp_valid = future_time1
                        chech_data.email_otp = otp
                        chech_data.save()

                    return Response(
                        {
                            "status": True,
                            "message": "OTP has been sent to your email address. Please check your mail otp="
                            + str(otp),
                        },
                        status=status.HTTP_200_OK,
                    )
            if recepient is not None and (otp is not None or otp != ""):
                chech_data = UserPropertyMailVerified.objects.filter(
                    user_id=user.id, email=recepient
                ).last()
            if chech_data is None:
                return Response(
                    {"status": False, "message": "Email is incorrect"},
                    status=status.HTTP_200_OK,
                )
            current_time = datetime.datetime.now()
            current_time1 = current_time.replace(tzinfo=pytz.utc)
            old_date_time = chech_data.email_otp_valid
            old_date_time1 = old_date_time.replace(tzinfo=pytz.utc)
            if current_time1 >= old_date_time1:
                return Response(
                    {"status": False, "message": "OTP expired."},
                    status=status.HTTP_200_OK,
                )
            if user_otp != chech_data.email_otp:
                return Response(
                    {"status": False, "message": "OTP is incorrect. please try again"},
                    status=status.HTTP_200_OK,
                )
            chech_data.property_code = "PRO" + str(uuid.uuid4().hex)[:8]
            chech_data.save()
            return Response(
                {
                    "status": True,
                    "message": "Property code has been sent to your email address. Please check your mail property_code="
                    + str(chech_data.property_code),
                },
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


class SearchAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FlashDealDetail
    serializer_class = FlashDealDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            result_data = {}
            query = self.request.GET.get("query", None)
            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)

            current_datetime = datetime.datetime.now()
            data = get_lat_long_calculated(lat, long, distance)
            print('current_datetime',current_datetime)
            property_id = (
                UserProperty.objects.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                .filter(long__gte=data.long2, long__lte=data.long1)
                .values_list("id", flat=True)
            )
            flash_deal = FlashDealDetail.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(deal_name__icontains=query)
                | Q(deal_type__name__icontains=query)
                | Q(deal_for__name__icontains=query)
                | Q(music_type__name__icontains=query)
                | Q(entry_type__name__icontains=query)
                | Q(drink_type__name__icontains=query)
                | Q(brand_type__name__icontains=query),
            ).distinct("id")
            result_data["flash_deal"] = FlashDealDetailSerializer(
                flash_deal, many=True
            ).data
            ###################
            deal = Deal.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(deal_name__icontains=query)
                | Q(deal_type__name__icontains=query)
                | Q(deal_for__name__icontains=query)
                | Q(music_type__name__icontains=query)
                | Q(entry_type__name__icontains=query)
                | Q(drink_type__name__icontains=query)
                | Q(brand_type__name__icontains=query),
            ).distinct("id")
            result_data["deal"] = DealSerializer(deal, many=True).data
            ######################
            party = Party.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(party_name__icontains=query)
                | Q(deal_type__name__icontains=query)
                | Q(deal_for__name__icontains=query)
                | Q(music_type__name__icontains=query)
                | Q(entry_type__name__icontains=query)
                | Q(drink_type__name__icontains=query)
                | Q(brand_type__name__icontains=query),
            ).distinct("id")
            result_data["party"] = PartySerializer(party, many=True).data

            response = {"status": True, "results": result_data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)



class FilterAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = FlashDealDetail
    serializer_class = FlashDealDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            result_data = {}
            deal_type = self.request.GET.get("deal_type", None)
            deal_for = self.request.GET.get("deal_for", None)
            music_type = self.request.GET.get("music_type", None)
            entry_type = self.request.GET.get("entry_type", None)
            drink_type = self.request.GET.get("drink_type", None)
            brand_type = self.request.GET.get("brand_type", None)

            deal_type = eval(deal_type) if deal_type is not None else []
            deal_for = eval(deal_for) if deal_for is not None else []
            music_type = eval(music_type) if music_type is not None else []
            entry_type = eval(entry_type) if entry_type is not None else []
            drink_type = eval(drink_type) if drink_type is not None else []
            brand_type = eval(brand_type) if brand_type is not None else []

            lat = request.query_params.get("lat", None)
            long = request.query_params.get("long", None)
            distance = request.query_params.get("distance", None)

            current_datetime = datetime.datetime.now()
            data = get_lat_long_calculated(lat, long, distance)
            print('current_datetime',current_datetime)
            property_id = (
                UserProperty.objects.filter(lat__gte=data.lat1, lat__lte=data.lat2)
                .filter(long__gte=data.long2, long__lte=data.long1)
                .values_list("id", flat=True)
            )
            flash_deal = FlashDealDetail.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(deal_type__id__in=deal_type)
                | Q(deal_for__id__in=deal_for)
                | Q(music_type__id__in=music_type)
                | Q(entry_type__id__in=entry_type)
                | Q(drink_type__id__in=drink_type)
                | Q(brand_type__id__in=brand_type),
            ).distinct("id")
            result_data["flash_deal"] = FlashDealDetailSerializer(
                flash_deal, many=True
            ).data
            ###################
            deal = Deal.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(deal_type__id__in=deal_type)
                | Q(deal_for__id__in=deal_for)
                | Q(music_type__id__in=music_type)
                | Q(entry_type__id__in=entry_type)
                | Q(drink_type__id__in=drink_type)
                | Q(brand_type__id__in=brand_type),
            ).distinct("id")
            result_data["deal"] = DealSerializer(deal, many=True).data
            ######################
            party = Party.objects.filter(
                Q(
                    property_id__in=property_id,
                    start_date__lte=current_datetime,
                    end_date__gte=current_datetime,
                ),
                Q(deal_type__id__in=deal_type)
                | Q(deal_for__id__in=deal_for)
                | Q(music_type__id__in=music_type)
                | Q(entry_type__id__in=entry_type)
                | Q(drink_type__id__in=drink_type)
                | Q(brand_type__id__in=brand_type),
            ).distinct("id")
            result_data["party"] = PartySerializer(party, many=True).data

            response = {"status": True, "results": result_data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {
                "status": False,
                "message": "Something Went Wrong",
                "error": str(e),
            }
            return Response(error, status=status.HTTP_200_OK)
