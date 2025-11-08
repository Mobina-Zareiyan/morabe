# Django Module
from django.db import models

# Third Party
from ckeditor.fields import RichTextField

# Local Module
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel

class Rules(AbstractDateTimeModel, AbstractBaseSeoModel):
    title = models.CharField(
        max_length=255,
        verbose_name='عنوان ',

    )

    class Meta:
        verbose_name = 'قوانین و مقررات',
        verbose_name_plural = 'قوانین و مقررات'

class RuleItem(models.Model):
    rules = models.ForeignKey(
        Rules,
        related_name='items',
        on_delete=models.CASCADE
    )
    topic = models.CharField(
        max_length=225,
        verbose_name='موضوع'
    )
    description = RichTextField(
        verbose_name='محتوا'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='ترتیب نمایش'
    )

    class Meta:
        verbose_name = 'آیتم قانون'
        ordering = ['order']









