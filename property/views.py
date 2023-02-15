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
from property.lat_long_calculator import get_lat_long_calculated
import json
import datetime
from property.models import *
from property.serializers import *
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


    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.filter(user=user.id)
            page = self.paginate_queryset(profile)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error":str(e)}
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
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                    request.data["property"] = serializer.data['id']
                    serializer_thumb = self.serializer_class_thumb(data=request.data)
                    if serializer_thumb.is_valid(raise_exception=False):
                        serializer_thumb.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_thumb.errors}, status=status.HTTP_200_OK
                        )
                    serializer_facility = self.serializer_class_facility(data=request.data)
                    if serializer_facility.is_valid(raise_exception=False):
                        serializer_facility.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_facility.errors}, status=status.HTTP_200_OK
                        )
                    serializer_social = self.serializer_class_social(data=request.data)
                    if serializer_social.is_valid(raise_exception=False):
                        serializer_social.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {"status": False, "error": serializer_social.errors}, status=status.HTTP_200_OK
                        )

                    return Response(
                        {"status": True, "results": serializer.data},
                        status=status.HTTP_200_OK,
                    )
                else:
                    transaction.set_rollback(True)
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
            response = self.serializer_class(profile,many=True)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error": str(e),}
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
                        {"status": False, "error": serializer.errors}, status=status.HTTP_200_OK
                    )
                facility = PropertyAvailableFacilities.objects.filter(property=kwargs["pk"]).last()
                request.data['property']=kwargs["pk"]
                serializer_facility = self.serializer_class_facility(instance=facility,data=request.data)
                if serializer_facility.is_valid(raise_exception=False):
                    serializer_facility.save()
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer_facility.errors}, status=status.HTTP_200_OK
                    )
                social = PropertySocialDetail.objects.filter(property=kwargs["pk"]).last()
                serializer_social = self.serializer_class_social(instance=social,data=request.data)
                if serializer_social.is_valid(raise_exception=False):
                    serializer_social.save()
                    return Response(
                        {"status": True, "message": "Successfully updated"}, status=status.HTTP_200_OK
                    )
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {"status": False, "error": serializer_social.errors}, status=status.HTTP_200_OK
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
            serializer = self.serializer_class(instance=property_social, data=request.data)
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
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
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
            serializer = self.serializer_class(instance=property_social, data=request.data)
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
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
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
                    {"status": True, "message":"Successfully created","results": serializer.data},
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
            user_id = self.request.GET.get('user_id', None)
            deal = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(deal)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False,
                    "message": "something went wrong", "error": str(e)}
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
                    {"status": True,"message":"Successfully Updated", "results": serializer.data},
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
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
            return Response(error, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
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
                    {"status": True, "message":"Successfully created","results": serializer.data},
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
            user_id = self.request.GET.get('user_id', None)
            profile = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(profile)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        except Exception as e:
            dict = {"status": False,
                    "message": "something went wrong", "error": str(e)}
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
                    {"status": True,"message":"Successfully Updated", "results": serializer.data},
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
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
            return Response(error, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
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
                    {"status": True, "message":"Successfully created","results": serializer.data},
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
            user_id = self.request.GET.get('user_id', None)
            party = self.queryset.filter(user=user_id)
            page = self.paginate_queryset(party)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            dict = {"status": False,
                    "message": "something went wrong", "error": str(e)}
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
                    {"status": True,"message":"Successfully Updated", "results": serializer.data},
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
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
            return Response(error, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        try:
            deal = self.queryset.get(pk=kwargs["pk"])
            deal.delete()
            response = {"status": True, "Message": "successfully deleted"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error": str(e)}
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
            lat = request.query_params.get('lat', None)
            long = request.query_params.get('long', None)
            distance = request.query_params.get('distance', None)
            date_range = request.query_params.get('date_range', None)
            if date_range is None or date_range == '':
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat,long,distance)
                property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                deal_inst = Deal.objects.filter(property__in=property_id,start_date__lte=current_datetime,end_date__gte=current_datetime)
            else:
                date_list = date_range.split(',')
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat,long,distance)
                    property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                    .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                    deal_id = Deal.objects.filter(property__in=property_id,start_date__date__lte=current_datetime,end_date__date__gte=current_datetime).values_list('id',flat=True)
                    deal_list.append(deal_id)
                deal_inst = Deal.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error":str(e)}
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
            lat = request.query_params.get('lat', None)
            long = request.query_params.get('long', None)
            distance = request.query_params.get('distance', None)
            date_range = request.query_params.get('date_range', None)
            if date_range is None or date_range == '':
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat,long,distance)
                property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                deal_inst = FlashDealDetail.objects.filter(property__in=property_id,start_date__lte=current_datetime,end_date__gte=current_datetime)
            else:
                date_list = date_range.split(',')
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat,long,distance)
                    property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                    .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                    deal_id = FlashDealDetail.objects.filter(property__in=property_id,start_date__date__lte=current_datetime,end_date__date__gte=current_datetime).values_list('id',flat=True)
                    deal_list.append(deal_id)
                deal_inst = FlashDealDetail.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error":str(e)}
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
            lat = request.query_params.get('lat', None)
            long = request.query_params.get('long', None)
            distance = request.query_params.get('distance', None)
            date_range = request.query_params.get('date_range', None)
            if date_range is None or date_range == '':
                current_datetime = datetime.datetime.now()
                data = get_lat_long_calculated(lat,long,distance)
                property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                deal_inst = Party.objects.filter(property__in=property_id,start_date__lte=current_datetime,end_date__gte=current_datetime)
            else:
                date_list = date_range.split(',')
                deal_list = []
                for date_ in date_list:
                    current_datetime = date_
                    data = get_lat_long_calculated(lat,long,distance)
                    property_id = self.queryset.filter(lat__gte=data.lat1, lat__lte=data.lat2)\
                    .filter(long__gte=data.long2, long__lte=data.long1).values_list('id',flat=True)
                    deal_id = Party.objects.filter(property__in=property_id,start_date__date__lte=current_datetime,end_date__date__gte=current_datetime).values_list('id',flat=True)
                    deal_list.append(deal_id)
                deal_inst = Party.objects.filter(id__in=list(set(deal_list)))
            page = self.paginate_queryset(deal_inst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong","error":str(e)}
            return Response(error, status=status.HTTP_200_OK)



