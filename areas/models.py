# Django Built-in modules
from django.db import models

# Local apps
from utils.models import AbstractDateTimeModel


class Province(AbstractDateTimeModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name= 'نام',
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name= 'طول',
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name= 'عرض',
    )

    class Meta:
        verbose_name =  'استان'
        verbose_name_plural =  'استان ها'

    def __str__(self):
        return self.name


class City(AbstractDateTimeModel):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name= 'استان',
    )
    name = models.CharField(
        max_length=255,
        verbose_name= 'نام',
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name= 'طول',
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name= 'عرض',
    )

    class Meta:
        unique_together = ('province', 'name',)
        verbose_name =  'شهر'
        verbose_name_plural =  'شهر ها'

    def __str__(self):
        return self.name
