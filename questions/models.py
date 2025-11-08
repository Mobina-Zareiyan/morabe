from django.db import models

from utils.models import AbstractDateTimeModel


class Category(models.TextChoices):
    REGISTRATION_AUTHENTICATION = "registration_auth", "ثبت‌نام و احراز هویت"
    INVESTMENT = "investment", "سرمایه‌گذاری"
    MARKET = "market", "بازار"


class FAQ(AbstractDateTimeModel):
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        verbose_name="دسته‌بندی موضوع"
    )
    question = models.CharField(
        max_length=255,
        verbose_name="صورت سؤال"
    )
    answer = models.TextField(
        verbose_name="پاسخ"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="نمایش در صفحه اصلی؟"
    )

    class Meta:
        verbose_name = "سؤال متداول"
        verbose_name_plural = "سؤالات متداول"
        ordering = ["-created"]

    def __str__(self):
        return self.question
