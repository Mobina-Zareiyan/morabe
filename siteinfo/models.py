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

    class Meta:
        verbose_name = 'پیکربندی سایت'
        verbose_name_plural = "پیکربندی سایت"





