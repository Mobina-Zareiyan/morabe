from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password
from .validators import (validate_mobile_number, validate_national_code, validate_national_code_unique,
                         validate_referral_code, validate_mobile_number_alg, validate_mobile_number_exist)


class RegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(required= True, max_length=11, validators=[validate_mobile_number])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    referral_code = serializers.CharField(required=False, allow_blank=True, validators=[validate_referral_code])
    national_code = serializers.CharField(validators= [validate_national_code, validate_national_code_unique])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_birth",
            "national_code",
            "mobile_number",
            "password",
            "referral_code",
        ]


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length= 11, validators=[validate_mobile_number_alg])
    password = serializers.CharField(write_only=True)


class PasswordResetCheckSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length= 11, validators=[validate_mobile_number_alg])


class SendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11, validators=[validate_mobile_number_exist])

class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()

class VerifyNationalCodeSerializer(serializers.Serializer):
    national_code = serializers.CharField(validators= [validate_national_code])

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password1 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password1']:
            raise serializers.ValidationError("رمزهای عبور مطابقت ندارند.")
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    national_code = serializers.CharField(validators= [validate_national_code, validate_national_code_unique])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_birth",
            "national_code",
            "mobile_number",
            "province",
            "city",
            "address",

        ]
        read_only_fields = ["mobile_number", ]


class ChangePasswordSerializer(serializers.Serializer):
    pre_password = serializers.CharField(write_only= True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password1 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password1']:
            raise serializers.ValidationError("رمزهای عبور مطابقت ندارند.")
        return attrs