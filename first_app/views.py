import base64
import io
import json
import requests
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer , MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView)
from .models import *
from distutils.command.config import config
from decouple import *
from .serializers import UserSerializer, MyTokenObtainPairSerializer, Obtain_Refresh_And_Access



# Register class
class RegisterView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            user_data_dic = JSONParser().parse(stream)
            if len(user_data_dic["recapcha"]) == 0:
                return Response({"message": "Recapcha invalid"}, status=status.HTTP_400_BAD_REQUEST)
            # secret = config('secret')
            secret = "6LdjEeQaAAAAAAFIGHyO4CzqEcsBrVKI0DeWFtwg"
            url = f"https://www.google.com/recaptcha/api/siteverify?secret={secret}&response={user_data_dic['recapcha']}"
            x = requests.post(url)
            response_dict = json.loads(x.text)
            # if response_dict["success"] == True:
            #     pass
            # else:
            #     return Response({"message": "Invalid capcha"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Recapcha Not provided !!! "},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if (Users.objects.get(email=user_data_dic.get('email'))):
                return Response({"Error": "Email", "message": "Email Already registered"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        json_data = request.body
        stream = io.BytesIO(json_data)
        user_data_dic = JSONParser().parse(stream)

        try:
            import uuid
            uuid = uuid.uuid4()
            user_data_dic['username'] = user_data_dic.get('first_name');
            user_data_dic['id'] = str(uuid);
            if Users.objects.get(id=str(uuid)):
                return Response({"message": "Internal Error !!! Try again"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        serializer = UserSerializer(data=user_data_dic)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Register successfully",
                "email": user_data_dic.get('email'),
                "username": user_data_dic.get('username'),
                "first_name": user_data_dic.get('first_name'),
                "last_name": user_data_dic.get('last_name'),
                "id": user_data_dic.get('id')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login class
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_data_of_user(request):
    try:
        return Response({"message":"welcome to dashboard"}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "credentials not provided !!"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('')
        response.delete_cookie('refresh')
        return response
    else:
        content = {'message': 'Request not allowed'}
        return Response(content)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_new_access_and_refrsh_token_and(request):
    try:
        if request.COOKIES.get('refresh'):
            token = request.COOKIES.get('refresh')
            splitted_token = token.split(".")
            second_base64_string = splitted_token[1]
            second_base64_string_bytes = second_base64_string.encode('ascii')
            jwt_bytes = base64.b64decode(second_base64_string_bytes + b'=' * (-len(second_base64_string_bytes) % 4))
            jwt_decoded = jwt_bytes.decode('ascii')
            jwt_decoded = json.loads(jwt_decoded)
            exp = jwt_decoded["exp"]
            import time
            time_expired_check = exp - time.time()
            if time_expired_check <= 0:
                return Response({"message": "Refresh token Expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if jwt_decoded["token_type"] != "refresh":
                return Response({"message": "Not valid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if jwt_decoded["user_id"] == request.user.id:
                pass
            else:
                return Response({"message": "Something went wrong in space"}, status=status.HTTP_400_BAD_REQUEST)
            user = Users.objects.get(id=request.user.id)
            refresh = Obtain_Refresh_And_Access.get_token(user)
            response = Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
            response.set_cookie('refresh', refresh, samesite="none", secure=True, httponly=True)
            return response
        else:
            response = Response({"message": "Refresh token missing !! "}, status=status.HTTP_400_BAD_REQUEST)
            return response
    except:
        response = Response({"message": "Something went wrong !! "}, status=status.HTTP_400_BAD_REQUEST)
        return response
