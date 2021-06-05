import base64
import json
import io
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from . import serializers
from .authentication import AUTH_HEADER_TYPES
from .exceptions import InvalidToken, TokenError
import socket
import requests
from distutils.command.config import config
from decouple import *


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    # =========================================================================
    def post(self, request, *args, **kwargs):
        if request.build_absolute_uri() == "http://api-v1-backend.herokuapp.com/api/token/":
            response = Response({"message": "Url was there"}, status=status.HTTP_200_OK)
            return response
        else:
            response = Response({"message": request.build_absolute_uri()}, status=status.HTTP_200_OK)
            return response
        try:
            if request.COOKIES:
                    request.COOKIES.clear()
            else:
                pass
        except:
            response = Response({"message": "Login Error !!!"}, status=status.HTTP_200_OK)
            return response
        if request.COOKIES.get('refresh'):
            serializer = self.get_serializer(data={"refresh": request.COOKIES.get('refresh')})
        else:
            serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        if request.COOKIES.get('refresh'):
            response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            try:
                refresh = serializer.validated_data.pop("refresh")
                response = Response(serializer.validated_data, status=status.HTTP_200_OK)
                response.set_cookie('refresh', refresh, samesite="none", secure=True, httponly=True)
            except:
                response = Response({"message": "something went wrong"}, status=status.HTTP_200_OK)
        return response
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #     except TokenError as e:
    #         raise InvalidToken(e.args[0])
    #
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainPairSerializer


token_obtain_pair = TokenObtainPairView.as_view()


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = serializers.TokenRefreshSerializer


token_refresh = TokenRefreshView.as_view()


class TokenObtainSlidingView(TokenViewBase):
    """
    Takes a set of user credentials and returns a sliding JSON web token to
    prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainSlidingSerializer


token_obtain_sliding = TokenObtainSlidingView.as_view()


class TokenRefreshSlidingView(TokenViewBase):
    """
    Takes a sliding JSON web token and returns a new, refreshed version if the
    token's refresh period has not expired.
    """
    serializer_class = serializers.TokenRefreshSlidingSerializer


token_refresh_sliding = TokenRefreshSlidingView.as_view()


class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = serializers.TokenVerifySerializer


token_verify = TokenVerifyView.as_view()
