# Django Built-in modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local apps
from utils.models import AbstractDateTimeModel


class SiteGlobalSetting(AbstractDateTimeModel):
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name= _('آدرس'),
    )
    map = models.TextField(
        null=True,
        blank=True,
        verbose_name= _('نقشه'),
        help_text= _('کد embed گوگل مپ'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name= _('ایمیل'),
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name= _('شماره تلفن')
    )
    fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name= _("درصد کارمزد")
    )

    tax_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name= _("درصد مالیات")
    )
    investment_pending_expire_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name= _("مدت زمان اعتبار پرداخت (دقیقه)"),
        help_text= _("مدت زمانی که کاربر برای پرداخت سرمایه‌گذاری فرصت دارد")
    )


    class Meta:
        verbose_name = _('پیکربندی سایت')
        verbose_name_plural = _("پیکربندی سایت")



class SocialMediaSetting(AbstractDateTimeModel):
    name = models.CharField(
        max_length=100,
        verbose_name= _('نام'),
    )
    username_or_id = models.CharField(
        max_length=100,
        verbose_name= _('نام کاربری یا آیدی'),
        help_text= _('مثال: firefly@'),
    )
    icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=
             _('به صورت پیشفرض از fontawesome پشتیبانی می شود، فقط کافیست نام آیکون را وارد کنید. برای مثال: facebook')
        ,
        verbose_name= _('آیکون'),
    )

    link = models.URLField(
        verbose_name= _('لینک'),
    )

    class Meta:
        verbose_name = _('شبکه اجتماعی')
        verbose_name_plural = _("شبکه های اجتماعی")

    def __str__(self):
        return self.name


