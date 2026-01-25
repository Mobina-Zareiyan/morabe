# Django Module
from django.db import models
from django.utils.translation import gettext_lazy as _


# Third Party
from ckeditor.fields import RichTextField

# Local Module
from utils.models import AbstractDateTimeModel


class Rules(AbstractDateTimeModel):
    title = models.CharField(
        max_length=255,
        verbose_name= _('عنوان'),
    )
    description = RichTextField(
        verbose_name=_('محتوا')
    )

    class Meta:
        verbose_name = _('قوانین و مقررات'),
        verbose_name_plural = _('قوانین و مقررات')







