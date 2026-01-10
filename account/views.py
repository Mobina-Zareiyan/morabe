from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.cache import cache
from account.models import User
from utils.services import send_normal_sms
from account.serializers import (RegisterSerializer, LoginSerializer, PasswordResetCheckSerializer,
                                 PasswordResetSerializer, ProfileSerializer)




class LoginRateThrottle(UserRateThrottle):
    rate = '5/min'

class OTPThrottle(AnonRateThrottle):
    rate = '3/min'

class RegisterView(generics.CreateAPIView):
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



class LoginView(generics.GenericAPIView):
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


class PasswordResetCheckView(generics.GenericAPIView):
    """
    بررسی کاربر و ارسال OTP برای ریست پسورد
    """
    serializer_class = PasswordResetCheckSerializer
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']

        try:
            user = User.objects.get(mobile_number=mobile)

            otp_code = get_random_string(length=6, allowed_chars='0123456789')

            # اینجا از cache جنگو استفاده کنم یا خودم بنویسم تا توی db ذخیره بشه و قابل پیگیری باشه؟
            cache.set(f"password_reset_otp_{mobile}", otp_code, 300)

            send_normal_sms(mobile, otp_code)

            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            #  همیشه پیام موفقیت بدهیم تا کسی نتونه بفهمد کاربر وجود دارد یا نه
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)




class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(mobile_number=mobile)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully"})
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
