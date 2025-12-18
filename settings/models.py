# Django Built-in modules
from django.db import models

# Local apps
from utils.models import AbstractDateTimeModel


class SiteGlobalSetting(AbstractDateTimeModel):
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name='آدرس',
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name='نقشه',
        help_text='کد embed گوگل مپ',
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='ایمیل',
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره تلفن'
    )
    fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="درصد کارمزد"
    )

    tax_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="درصد مالیات"
    )
    investment_pending_expire_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name="مدت زمان اعتبار پرداخت (دقیقه)",
        help_text="مدت زمانی که کاربر برای پرداخت سرمایه‌گذاری فرصت دارد"
    )


    class Meta:
        verbose_name = 'پیکربندی سایت'
        verbose_name_plural = "پیکربندی سایت"



class SocialMediaSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=100,
        verbose_name='نام',
    )
    username_or_id = models.CharField(
        max_length=100,
        verbose_name='نام کاربری یا آیدی',
        help_text='مثال: firefly@',
    )
    icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=
            'به صورت پیشفرض از fontawesome پشتیبانی می شود، فقط کافیست نام آیکون را وارد کنید. برای مثال: facebook'
        ,
        verbose_name='آیکون',
    )

    link = models.URLField(
        verbose_name='لینک',
    )

    class Meta:
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = "شبکه های اجتماعی"

    def __str__(self):
        return self.name


