from django.core.exceptions import ValidationError
import re
from .models import User
def validate_national_code(value):
    """
    اعتبارسنجی کد ملی ایران بر اساس الگوریتم رقم‌کنترل
    """

    # فقط اعداد و طول 10
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("کد ملی باید شامل ۱۰ رقم باشد.")

    # جلوگیری از کدهای جعلی تکراری مثل 1111111111
    if value in [
        "0000000000", "1111111111", "2222222222", "3333333333", "4444444444",
        "5555555555", "6666666666", "7777777777", "8888888888", "9999999999"
    ]:
        raise ValidationError("کد ملی معتبر نیست.")

    check = int(value[9])  # رقم کنترل
    s = sum(int(value[i]) * (10 - i) for i in range(9))  # محاسبه مجموع وزنی
    r = s % 11  # باقیمانده

    # اعتبارسنجی نهایی
    if not ((r < 2 and check == r) or (r >= 2 and check == 11 - r)):
        raise ValidationError("کد ملی معتبر نیست.")


def validate_mobile_number(value):
    """
    اعتبارسنجی شماره موبایل ایران
    """
    pattern = r'^09\d{9}$'  # الگوی شماره موبایل ایران

    if not re.match(pattern, value):
        raise ValidationError("شماره موبایل معتبر نیست")
    if User.objects.filter(mobile=value).exists():
        raise ValidationError("این شماره موبایل قبلاً ثبت شده است.")

    return value


def validate_mobile_number_alg(value):
    """
    اعتبارسنجی شماره موبایل ایران
    """
    pattern = r'^09\d{9}$'  # الگوی شماره موبایل ایران

    if not re.match(pattern, value):
        raise ValidationError("شماره موبایل معتبر نیست")

    return value


def validate_mobile_number_exist(value):
    """
    بررسی عضویت کاربر با این شماره موبایل
    """

    if User.objects.filter(mobile=value).exists():
        raise value

    return ValidationError("این شماره موبایل قبلاً ثبت نشده است.")




def validate_national_code_unique(value):
    validate_national_code(value)  # چک الگوریتم
    if User.objects.filter(national_code=value).exists():
        raise ValidationError("این کد ملی قبلاً ثبت شده است")
    return value


def validate_referral_code(value):
    if value and not User.objects.filter(referral_code=value).exists():
        raise ValidationError("کد معرف معتبر نیست")
    return value

