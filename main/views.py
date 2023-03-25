from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.serializers import (UserRegistrationSerializer, 
                              UserLoginSerializer, 
                              UserProfileSerializer, 
                              UserChangePasswordSerializer,
                              RequestPasswordResetSerializer,
                              UserPasswordResetSerializer,
                              )

from main.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format = False):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception= True):
            user = serializer.save()
            return Response({'msg' :"Registration Successs"},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer] #customize message display
    def post(self, request, format = False):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        print(email,password,request.data,serializer.data.get('password'))
        user = authenticate(email = email, password = password)
        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg' :"Login Successs",'token':token},status=status.HTTP_201_CREATED)
        
        return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status = status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' :"Password changed Successsfully."},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserRequestPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        serializers = RequestPasswordResetSerializer(data = request.data)
        if(serializers.is_valid()):
            uid = serializers.get_user_id()
            token = serializers.get_token_for_password_reset()
            
            return Response({'uid':uid,'token':token}, status = status.HTTP_200_OK)
        
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None):
        serializers = UserPasswordResetSerializer(data = request.data,context = {'uid':uid,'token':token})
        if serializers.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successfully.'}, status = status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)