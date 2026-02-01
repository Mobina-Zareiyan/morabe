# Django Built-in Modules
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Apps
from utils.models import AbstractDateTimeModel
from seo.models import AbstractBaseSeoModel



class Category(AbstractBaseSeoModel, AbstractDateTimeModel):
    name = models.CharField(
        max_length= 225,
        unique= True,
        verbose_name= _('نام دسته‌بندی')
    )

    class Meta:
        verbose_name = _("دسته‌بندی")
        verbose_name_plural = _("دسته‌بندی‌ها")
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def default_search_engine_title(self):
        return self.name


class FAQ(AbstractDateTimeModel):
    category = models.ForeignKey(
        'Category',
        on_delete= models.CASCADE,
        related_name="faqs",
        verbose_name= _("دسته‌بندی موضوع")
    )
    question = models.CharField(
        max_length=255,
        verbose_name= _("صورت سؤال")
    )
    answer = models.TextField(
        verbose_name= _("پاسخ")
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name= _("نمایش در صفحه اصلی؟")
    )

    class Meta:
        verbose_name = _("سؤال متداول")
        verbose_name_plural = _("سؤالات متداول")
        ordering = ["-created"]

    def __str__(self):
        return self.question
