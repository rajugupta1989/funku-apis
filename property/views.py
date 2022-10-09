from django.shortcuts import render
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
from property.models import *
from property.serializers import *

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


class AddPropertyAPIView(generics.CreateAPIView):
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
            instance = self.queryset.filter(user_id=user_id)
            serializer = self.serializer_class(instance, many=True)
            dict = {'status': True, 'results': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
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
            instance = self.queryset.filter(user_id=user_id)
            serializer = self.serializer_class(instance, many=True)
            dict = {'status': True, 'results': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
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
            instance = self.queryset.filter(user_id=user_id)
            serializer = self.serializer_class(instance, many=True)
            dict = {'status': True, 'results': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
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