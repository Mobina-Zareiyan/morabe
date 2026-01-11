# Django Module
from django.db import models
from django.utils.translation import gettext_lazy as _


# Third Party
from ckeditor.fields import RichTextField

# Local Module
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel

class Rules(AbstractDateTimeModel, AbstractBaseSeoModel):
    title = models.CharField(
        max_length=255,
        verbose_name= _('عنوان'),
    )

    class Meta:
        verbose_name = _('قوانین و مقررات'),
        verbose_name_plural = _('قوانین و مقررات')

class RuleItem(models.Model):
    rules = models.ForeignKey(
        Rules,
        related_name='items',
        on_delete=models.CASCADE
    )
    topic = models.CharField(
        max_length=225,
        verbose_name= _('موضوع')
    )
    description = RichTextField(
        verbose_name= _('محتوا')
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name= _('ترتیب نمایش')
    )

    class Meta:
        verbose_name = _('آیتم قانون')
        verbose_name_plural = _('آیتم های قانون')
        ordering = ['order']









