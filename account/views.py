from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserViewSerializer
from account.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user)
                result = dict()
                result['data'] = serializer.data
                result['token'] = token
                return Response({"status":True, "result":result, "message":"User Registered Successfully !"})
            else:
                return Response({"status":False, "result":serializer.errors, "message":"User not Registered Successfully !"})
        except Exception as error:
            return Response({"status":False, "result":serializer.errors, "message":"User not Registered Successfully !"})


class UserLoginView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = authenticate(email=email, password=password)
                result = dict()
                if user is not None:
                    token = get_tokens_for_user(user)
                    result = dict()
                    result['data'] = token
                    return Response({"status":True, "result":result, "message":"User Logged In Successfully !"})
                else:
                    return Response({"status":False, "message":"Email & Password Doesn't Match !"}) 
            else:
                return Response({"status":False, "result":serializer.errors, "message":"User not Logged In Successfully !"})
        except Exception as error:
            return Response({"status":False, "result":serializer.errors, "message":"User not Logged In Successfully !"})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def User_view(request, name=None):
    get_obj = User.objects.get(name=name)
    serializer = UserViewSerializer(get_obj)
    if serializer:
        result = dict()
        result['data'] = serializer.data
        return Response({"status":True, "result":result, "message":"Records fetched Successfully !"})
    else:
        return Response({"status":False, "result":dict(), "message":"Records not fetched Successfully !"})


