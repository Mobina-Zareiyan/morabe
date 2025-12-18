
from django.db import models
from django.db.models import Q, UniqueConstraint

from project.models import Project
from account.models import User
from utils.models import AbstractDateTimeModel


class Investment(AbstractDateTimeModel):
    user = models.ForeignKey(
        User,
        null= True,
        blank= True,
        on_delete= models.SET_NULL,
        related_name= 'investments',
        verbose_name= 'کاربر',
    )
    project = models.ForeignKey(
        Project,
        null=True,
        blank= True,
        on_delete= models.SET_NULL,
        related_name= 'investments',
        verbose_name= 'پروژه'
    )
    area = models.DecimalField(
        max_digits= 10,
        decimal_places= 3,
        verbose_name= 'مساحت'
    )
    price_per_meter = models.PositiveIntegerField(
        verbose_name= 'قیمت هر متر'
    )
    base_amount = models.PositiveIntegerField(
        verbose_name= 'مبلغ خرید'
    )
    fee_amount = models.PositiveIntegerField(
        verbose_name= 'کارمزد'
    )
    tax_amount = models.PositiveIntegerField(
        verbose_name= 'مالیات'
    )
    total_payment = models.PositiveIntegerField(
        verbose_name= 'مبلغ قابل پرداخت'
    )
    status = models.CharField(
        max_length= 50,
        choices= (
            ('pending', 'در انتظار پرداخت'),
            ('paid', 'پرداخت شده'),
            ('canceled', 'لغو شده'),
        ),
        default = 'pending'
    )
    expires_at = models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= 'زمان انقضای پرداخت',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "project"],
                condition=Q(status="pending"),
                name="unique_pending_investment"
            )
        ]
        verbose_name = "سرمایه‌گذاری"
        verbose_name_plural = "سرمایه‌گذاری‌ها"



    def __str__(self):
        return f"{self.user.fullname if self.user else '-'} | {self.project.title if self.project else '-'}"


