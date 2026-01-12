import string
from django.utils.crypto import get_random_string
from django.contrib.auth.models import BaseUserManager


# -----------------------------
#   تابع تولید کد معرف یکتا
# -----------------------------
def generate_referral_code(length=8):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = get_random_string(length= length, allowed_chars= chars)
        if not "User".objects.filter(referral_code=code).exists():
            return code


# -----------------------------
#         UserManager
# -----------------------------
class UserManager(BaseUserManager):

    def create_user(self, mobile_number, password= None, **extra_fields):

        required_fields = ['first_name', 'last_name', 'date_birth', 'national_code',]

        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'کاربر باید {field} داشته باشد.')

        user = self.model(
            mobile_number=mobile_number,
            **extra_fields
        )

        user.referral_code = generate_referral_code()
        user.set_password(password)
        # بود و نبود این چه فرقی داره؟
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # فیلدهای اجباری
        required_fields = ['first_name', 'last_name',
                           'date_birth', 'national_code']

        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'Superuser must have {field}')

        return self.create_user(mobile_number, password, **extra_fields)
