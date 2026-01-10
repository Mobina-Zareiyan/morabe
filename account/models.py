# Django Built-in modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse

# Local apps
from utils.models import AbstractDateTimeModel, AbstractUUIDModel
from .managers import UserManager
# Python Standard Library
import uuid as _uuid



class User(AbstractBaseUser, AbstractDateTimeModel, AbstractUUIDModel, PermissionsMixin):
    """
    This models inherits from django base user.
    """
    # اگه این نباشه جنگو پیش فرض از اعداد ترتیبی استفادهه میکنه
    uuid = models.UUIDField(unique=True, default=_uuid.uuid4, editable=False)
    first_name = models.CharField(
        max_length=200,
        verbose_name='نام',
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='نام خانوادگی',
    )
    date_birth = models.DateField(
        verbose_name= 'تاریخ تولد',
    )
    national_code = models.CharField(
        max_length=10,
        verbose_name= 'کدملی',
    )
    mobile_number = models.CharField(
        max_length=11,
        unique= True,
        verbose_name='شماره موبایل',
    )
    province = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= 'استان',
    )
    city = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= 'شهر',
    )
    address = models.CharField(
        max_length= 225,
        null= True,
        blank= True,
        verbose_name= 'آدرس',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='فعال',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='ادمین',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='کارمند',
    )
    referral_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='کد معرف'
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='referrals',
        verbose_name='معرف'
    )
    # video

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
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.mobile_number

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def is_admin(self):
        return self.is_superuser and self.is_staff


