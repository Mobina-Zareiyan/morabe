# Django Built-in modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils import timezone



# Local apps
from utils.models import AbstractDateTimeModel, AbstractUUIDModel
from .managers import UserManager
from utils.services import send_normal_sms


# Python Standard Library
import uuid as _uuid
import random
import qrcode
from io import BytesIO
import base64
import string
from datetime import timedelta



class User(AbstractBaseUser, AbstractDateTimeModel, AbstractUUIDModel, PermissionsMixin):
    """
    This models inherits from django base user.
    """
    # اگه این نباشه جنگو پیش فرض از اعداد ترتیبی استفاده میکنه
    uuid = models.UUIDField(unique=True, default=_uuid.uuid4, editable=False)
    first_name = models.CharField(
        max_length=200,
        verbose_name= _('نام'),
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name= _('نام خانوادگی'),
    )
    date_birth = models.DateField(
        verbose_name= _('تاریخ تولد'),
    )
    national_code = models.CharField(
        max_length=10,
        verbose_name= _('کدملی'),
    )
    mobile_number = models.CharField(
        max_length=11,
        unique= True,
        verbose_name= _('شماره موبایل'),
    )
    province = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= _('استان'),
    )
    city = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= _('شهر'),
    )
    address = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= _('آدرس'),
    )
    is_active = models.BooleanField(
        default= True,
        verbose_name= _('فعال'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name= _('ادمین'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name= _('کارمند'),
    )
    is_authenticate = models.BooleanField(
        default= False,
        verbose_name= _('احراز هویت')
    )
    referral_code = models.CharField(
        max_length=10,
        null= True,
        blank= True,
        unique=True,
        verbose_name= _('کد معرف')
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='referrals',
        verbose_name= _('معرف')
    )
    video = models.FileField(
        null= True,
        blank= True,
        upload_to= 'account/%y/%m/%d/',
        editable= True,
        verbose_name= _("ویدئو احراز هویت")
    )
    seryal = models.CharField(
        max_length= 10,
        null= True,
        blank= True,
        verbose_name= _("سریال کارت ملی")
    )
    qr_code_base64 = models.CharField(
        max_length= 255,
        null= True,
        blank= True,
        verbose_name= _("QR کد")
    )


    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = [
    "first_name",
    "last_name",
    "date_birth",
    "national_code",
    ]

    # ???
    objects = UserManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        return self.mobile_number

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def is_admin(self):
        return self.is_superuser and self.is_staff


    def create_qr_code(self):
        """Generate base64 QR code linking to the scan URL"""
        qr = qrcode.make(self.referral_code)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        qr_image = buffer.getvalue()
        qr_base64 = base64.b64encode(qr_image).decode('utf-8')
        print("*********************")
        return f"data:image/png;base64,{qr_base64}"


    def create_referral_code(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            code = get_random_string(length=8, allowed_chars=chars)
            if not User.objects.filter(referral_code=code).exists():
                return code



    def save(self, *args, **kwargs):
        if not self.qr_code_base64:
            self.qr_code_base64 = self.create_qr_code()

        if not self.referral_code:
            self.referral_code = self.create_referral_code()

        super().save(*args, **kwargs)



class OtpCode(AbstractDateTimeModel):
    phone_number = models.CharField(
        max_length= 11,
        verbose_name= _("شماره موبایل")
    )
    code = models.PositiveSmallIntegerField(
        verbose_name= _("کد")
    )
    is_active = models.BooleanField(
        default= True,
        verbose_name= _("فعال")
    )
    is_verified = models.BooleanField(
        default= False,
        verbose_name= _("احراز شده")
    )
    expires_at = models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= _("انقضا")
    )

    @classmethod
    def send_otp(cls, phone):
        random_code = random.randint(100000, 999999)
        cls.objects.filter(phone_number=phone, is_active=True).update(is_active=False)
        expiration_time = timezone.now() + timedelta(minutes= 5)

        send_normal_sms(phone, random_code)
        cls.objects.create(
            phone_number=phone,
            code=random_code,
            expires_at= expiration_time
        )

    @classmethod
    def verify_otp(cls, phone, code):
        try:
            otp = cls.objects.get(phone_number= phone, code= code, is_active= True)
            if otp.expires_at < timezone.now():
                otp.is_active = False
                otp.save()
                return {"success": False, "error": "کد منقضی شده است"}
            otp.is_verified = True
            otp.is_active = False
            otp.save()
            return {"success": True}
        except cls.DoesNotExist:
            return {"success": False, "error": "کد نامعتبر است"}

    class Meta:
        ordering = ('-created',)
        verbose_name = _("کد یکبار مصرف")
        verbose_name_plural = _("کدهای یکبار مصرف")

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'

