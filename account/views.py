# Django Module
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.cache import cache

# Local Module
from account.models import User, OtpCode
from utils.services import send_normal_sms
from account.serializers import (RegisterSerializer, LoginSerializer, PasswordResetCheckSerializer,
                                 PasswordResetSerializer, ProfileSerializer, PasswordResetCheckMobileSerializer,
                                 VerifyCodeSerializer, VerifyNationalCodeSerializer, ChangePasswordSerializer)




class LoginRateThrottle(UserRateThrottle):
    rate = '5/min'

class OTPThrottle(AnonRateThrottle):
    rate = '3/min'



class RegisterAPIView(generics.CreateAPIView):
    """
    برای ثبت نام توی سامانه
    """

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginRateThrottle, AnonRateThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            mobile_number=serializer.validated_data['mobile_number'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # if not user.is_active:
        #     return Response({"detail": "User account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class SendOTPAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetCheckMobileSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
        request.session['mobile'] = {
            'phone_number': mobile,
        }

        try:
            user = User.objects.filter(mobile_number= mobile)
            OtpCode.send_otp(mobile)
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)


        except User.DoesNotExist:
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        user_session = request.session['mobile']

        try:
            code_instance = OtpCode.objects.get(phone_number= user_session['phone_number'])
        except OtpCode.DoesNotExist:
            return Response({'error':'code not found'}, status= status.HTTP_404_NOT_FOUND)

        ser_data = VerifyCodeSerializer(data= request.data)
        ser_data.is_valid(raise_exception= True)
        cd = ser_data.validated_data
        if cd['code'] == code_instance:

            code_instance.is_active = False
            code_instance.save()

            return Response({"detail": "This code is correct"}, status=status.HTTP_200_OK)

        return Response({'error': 'This code is wrong'}, status=status.HTTP_400_BAD_REQUEST)



class VerifyNationalCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyNationalCodeSerializer

    def post(self, request):
        user_session = request.session['mobile']
        mobile = user_session['phone_number']
        user = User.objects.filter(mobile_number= mobile)
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        national_code = serializer.validated_data['national_code']
        if user.national_code == national_code:
            return Response({"detail": "You can change your password"}, status=status.HTTP_200_OK)

        return Response({'error': 'This code is wrong'}, status=status.HTTP_400_BAD_REQUEST)



# class PasswordResetCheckAPIView(generics.GenericAPIView):
#     """
#     بررسی کاربر و ارسال OTP برای ریست پسورد
#     """
#     serializer_class = PasswordResetCheckSerializer
#     throttle_classes = [LoginRateThrottle]
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         mobile = serializer.validated_data['mobile_number']
#         user = User.objects.get(mobile_number=mobile)
#
#         try:
#
#             otp_code = get_random_string(length=6, allowed_chars='0123456789')
#
#             # اینجا از cache جنگو استفاده کنم یا خودم بنویسم تا توی db ذخیره بشه و قابل پیگیری باشه؟
#             cache.set(f"password_reset_otp_{mobile}", otp_code, 300)
#
#             send_normal_sms(mobile, otp_code)
#
#             return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
#
#         except user.DoesNotExist:
#             #  همیشه پیام موفقیت بدهیم تا کسی نتونه بفهمد کاربر وجود دارد یا نه
#             return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
#



class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        user_session = request.session['mobile']
        mobile = user_session['phone_number']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(mobile_number=mobile)
            user.set_password(new_password)
            user.save()
            del request.session['mobile']
            return Response({"detail": "Password updated successfully"})
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)





class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    parser_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        user = request.user
        pre_password = serializer.validated_data['pre_password']

        if user.password == pre_password:
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            return Response({"detail": "Password updated successfully"})
        return Response({"detail": "The password is incorrect"})


