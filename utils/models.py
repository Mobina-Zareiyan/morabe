# Django Module
from django.db import models
from django.contrib import admin

# Third Party
from .jdatetime import standard_jalali_datetime_format, pretty_jalali_datetime_format





class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name= 'ایجاد شده',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name= 'آپدیت شده',
    )

    class Meta:
        abstract = True

    @admin.display(description='ایجاد شده' , empty_value='-')
    def jcreated(self):
        return standard_jalali_datetime_format(self.created)

    @admin.display(description='ایجاد شده' , empty_value='-')
    def jpcreated(self):
        return pretty_jalali_datetime_format(self.created)

    jcreated.admin_order_field = 'created'

    @admin.display(description= 'آپدیت شده' , empty_value='-')
    def jupdated(self):
        return standard_jalali_datetime_format(self.updated)

    jupdated.admin_order_field = 'updated'

