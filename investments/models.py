# Django Module
from django.db import models
from django.db.models import Q, UniqueConstraint

# Third Party Module
from validators import ValidationError

# Local Module
from project.models import Project
from account.models import User
from utils.models import AbstractDateTimeModel


class Investment(AbstractDateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete= models.PROTECT,
        related_name= 'investments',
        verbose_name= 'کاربر',
    )
    project = models.ForeignKey(
        Project,
        on_delete= models.PROTECT,
        related_name= 'investments',
        verbose_name= 'پروژه'
    )
    area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
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
    sold_area = models.DecimalField(
        max_digits=14,
        decimal_places=6,
        default=0,
        verbose_name='متراژ فروخته شده',
    )
    locked_area = models.DecimalField(
        max_digits=14,
        decimal_places=6,
        default=0,
        help_text="متراژی که در sale های فعال قفل شده"
    )




    @property
    def remaining_area(self):
        return self.area - self.sold_area - self.locked_area

    class Meta:
        # اینجا ممکن هست که کاربر یدونه pending الکی داشته باشه و بعدا بخاطرش نتونه دیگه خریدی انجام بده؟؟؟
        # بررسی کنم ببینم جایی هست که بعد از حذف درخواست قبلی pending رو براش ممنقضی نکنه
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
        return (f"{self.user.fullname if self.user else '-'} | {self.project.title if self.project else '-'} |"
                f" {self.area} | {self.status}")




class InvestmentSale(AbstractDateTimeModel):

    investment = models.ForeignKey(
        Investment,
        on_delete= models.PROTECT,
        related_name= 'sales',
        verbose_name= 'سرمایه گذاری مرجع'
    )
    seller = models.ForeignKey(
        User,
        on_delete= models.PROTECT,
        related_name= 'sales',
        verbose_name= 'فروشنده'
    )
    buyer = models.ForeignKey(
        User,
        null= True,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name='خریدار',
    )
    price_per_meter = models.PositiveIntegerField(
        verbose_name= 'قیمت هر متر',
    )
    selling_area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
        verbose_name= 'متراژ قابل فروش'
    )
    status = models.CharField(
        max_length= 50,
        choices= (
            ('selling','در انتظار فروش'),
            ('sold', 'فروخته شده'),
            ('canceled', 'کنسل شده'),
        ),
        default= 'selling'
    )
    sold_at = models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= 'تاریخ فروش',
    )
    # مبلغی که خریدار وارد میکنه (محاسبه متراژ و ... برعهده منه)
    base_amount = models.PositiveIntegerField(
        verbose_name= 'مبلغ خرید کاربر',
    )
    sale_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='انقضای فروش'
    )
    sold_area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
        default= 0,
        verbose_name= 'متراژ فروخته شده',
    )
    fee_amount = models.PositiveIntegerField(
        verbose_name='کارمزد'
    )
    tax_amount = models.PositiveIntegerField(
        verbose_name='مالیات'
    )
    total_payment = models.PositiveIntegerField(
        verbose_name='مبلغ قابل پرداخت'
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='زمان انقضای پرداخت',
    )


    def clean(self):
        if self.sold_area and self.selling_area:
            if self.sold_area > self.selling_area:
                raise ValidationError("متراژ فروخته شده نمی‌تواند از متراژ قابل فروش بیشتر باشد")



    @property
    def remaining_area(self):
        return self.selling_area - self.sold_area


    class Meta:
        verbose_name = "فروش سرمایه‌گذاری"
        verbose_name_plural = "فروش سرمایه‌گذاری‌ها"

    def __str__(self):
        return f"{self.investment} | {self.seller}  | {self.status} "






