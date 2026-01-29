# Django Built-in Modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel

# Third Party Packages
from ckeditor.fields import RichTextField




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







