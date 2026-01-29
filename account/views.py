# Django Module
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Local Module
from account.models import User, OtpCode
from account.serializers import (RegisterSerializer, LoginSerializer, ChangePasswordSerializer,
                                 PasswordResetSerializer, ProfileSerializer, SendOTPSerializer,
                                 VerifyCodeSerializer, VerifyNationalCodeSerializer, VerifyAuthenticationSerializer)




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

        if not user.is_active:
            return Response({"detail": "User account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class SendOTPAPIView(generics.GenericAPIView):
    serializer_class = SendOTPSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
        code = serializer.validated_data['code']

        result = OtpCode.verify_otp(mobile, code)

        if result['success']:
            return Response({"detail": "کد صحیح است."}, status= status.HTTP_200_OK)
        else:
            return Response({"error": result['error']}, status= status.HTTP_400_BAD_REQUEST)



class VerifyNationalCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyNationalCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
        user = User.objects.get(mobile_number= mobile)
        national_code = serializer.validated_data['national_code']
        if user.national_code == national_code:
            return Response({"detail": "You can change your password"}, status=status.HTTP_200_OK)

        return Response({'error': 'This code is wrong'}, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile_number']
        new_password = serializer.validated_data['new_password']
        otp = OtpCode.objects.filter(
            phone_number=mobile,
            is_verified=True,
            is_active=False,
            expires_at__gte=timezone.now()
        ).order_by("-created").first()

        if not otp:
            return Response({"error": "مراحل احراز هویت کامل نشده است"},status=status.HTTP_403_FORBIDDEN)


        try:

            user = User.objects.get(mobile_number=mobile)
            user.set_password(new_password)
            user.save()
            otp.is_verified = False
            otp.save()
            return Response({"detail": "Password updated successfully"}, status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)






class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        user = request.user
        pre_password = serializer.validated_data['pre_password']

        if user.check_password(pre_password):
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            return Response({"detail": "Password updated successfully"})
        return Response({"detail": "The password is incorrect"})





class AuthenticationVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyAuthenticationSerializer(request.user, data= request.data, partial= True)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response({"detail": _('اطلاعات احراز هویت ارسال شد')}, status=status.HTTP_200_OK)
