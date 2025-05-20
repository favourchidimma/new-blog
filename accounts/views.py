from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView 
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from .models import*
from rest_framework.permissions import IsAuthenticated
import random
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

def generate_otp():

    otp = random.randint(000000, 999999)


    return otp

User = get_user_model()

class UserGenericView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]


    def create(self, request, *args, **kwargs):


       serializer = UserSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)


       User.objects.create_user(
           **serializer.validated_data
       ) 


       return Response(serializer.data, status=201)
    
    def get (self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials not valid"})
        
        users = User.objects.all()

        return Response(UserSerializer(users, many=True).data, status=200)
     
class UserGenericByOne(generics.RetrieveDestroyAPIView):
    serializer_class= UserSerializer
    queryset = User.objects.all()
    lookup_field='pk'  


class OtpVerifyView(APIView):

    @swagger_auto_schema(methods=['POST'], request_body=OtpSerializer)
    @action(detail=True, methods=['POST'])

    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']


        if not OTP.objects.filter(otp = otp).exists():

            return Response({"error": "otp not found or invalid"}, status=404)
        
        otp = OTP.objects.get(otp = otp)

        if otp.is_otp_valid():

            otp.user.is_active = True
            otp.user.save()

            otp.delete()

            return Response({"message": "User successfully verified"}, status=200)
        
        else:

            otp.delete()

            return Response({"error": "otp is expired"}, status=400)
class LoginView(APIView):

    @swagger_auto_schema(methods=['POST'], request_body=LoginSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):

        serializer= LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)


        user = authenticate(
            request,
            email = serializer.validated_data.get('email'),
            password = serializer.validated_data.get('password')
        )

        if user:
            
            token_data = RefreshToken.for_user(user)
            
            
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'refresh': str(token_data),
                'access': str(token_data.access_token)
            }




            return Response(data, status=200)
        return Response({"error": "invalid email or password"}, status=400)
    

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=404)
        
        
        otp_code = generate_otp()
        expiry = timezone.now() + timezone.timedelta(minutes=10)
        
       
        OTP.objects.create(
            otp=str(otp_code),
            user=user,
            expiry_date=expiry
        )
        
        url = "https://api.useplunk.com/v1/track"
        headers = {
            "Authorization": "Bearer sk_10c4a02e1119df59dedfc538c730b4e437b997aa7ff781f0",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "event": "password_reset",
            "data": {
                "full_name": user.first_name,
                "otp": str(otp_code)
            }
        }
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        
        return Response({"message": "OTP sent to your email."})


class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_user(self):
        
        return self.request.user
    
    def update_password(self, request, *arg, **kwargs):
        
        serializer = PasswordChangeSerializer(data=request.data, context={'request':request})
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({'message':'password has been successfully updated'}, status=200)
    
class LogoutView(APIView):
    
    def post(self, request):
        
        try:
            refresh_token= request.data['refresh']
            token = RefreshToken(refresh_token)
            
            token.blacklist()
            
            return Response('User Logged-out', status= 205)
        
        except Exception:
            
            return Response('request failed', status=400)
        



