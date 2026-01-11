# Django built-in
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel


class ContactUsMessages(AbstractDateTimeModel):
    full_name = models.CharField(
        max_length=50,
        verbose_name= _('نام و نام خانوادگی'),
    )
    email = models.EmailField(
        verbose_name=_('ایمیل'),
    )
    phone = models.CharField(
        max_length=11,
        verbose_name= _('شماره تماس'),
        blank=True,
        null=True,
    )
    message = models.TextField(
        verbose_name= _('پیام'),
    )
    is_checked = models.BooleanField(
        default=False,
        verbose_name= _('بررسی شده؟'),
    )

    class Meta:
        verbose_name = _('پیام')
        verbose_name_plural = _("پیام ها")
        ordering = ('-created',)

    def __str__(self):
        return f'{self.full_name} - {self.email}'
