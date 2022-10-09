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
from promoter.models import *
from promoter.serializers import *




class AddPromoterAPIView(generics.CreateAPIView):
    """
    Add promoter
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserPromoter.objects.all()
    serializer_class = UserPromoterSerializer

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


class UpdatePromoterAPIView(generics.RetrieveUpdateAPIView):
    """
    Update promoter
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserPromoter.objects.all()
    serializer_class = UserPromoterSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            request.data["user"] = user.id
            profile = self.queryset.get(pk=kwargs["pk"])
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
            profile = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)



class AddPromoterSocialProfileAPIView(generics.CreateAPIView):
    """
    Add Promoter social profile
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PromoterSocialProfile.objects.all()
    serializer_class = PromoterSocialProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
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


class UpdatePromoterSocialProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Promoter social profile Update
    """

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = PromoterSocialProfile.objects.all()
    serializer_class = PromoterSocialProfileSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user = self.request.user
            profile = self.queryset.get(pk=kwargs["pk"])
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
            profile = self.queryset.get(pk=kwargs["pk"])
            response = self.serializer_class(profile)
            response = {"status": True, "results": response.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error = {"status": False, "message": "Something Went Wrong"}
            return Response(error, status=status.HTTP_200_OK)