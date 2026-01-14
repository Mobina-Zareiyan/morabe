# Django Module
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _


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
        verbose_name= _('کاربر'),
    )
    project = models.ForeignKey(
        Project,
        on_delete= models.PROTECT,
        related_name= 'investments',
        verbose_name= _('پروژه')
    )
    area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
        verbose_name= _('مساحت')
    )
    price_per_meter = models.PositiveIntegerField(
        verbose_name= _('قیمت هر متر')
    )
    base_amount = models.PositiveIntegerField(
        verbose_name= _('مبلغ خرید')
    )
    fee_amount = models.PositiveIntegerField(
        verbose_name= _('کارمزد')
    )
    tax_amount = models.PositiveIntegerField(
        verbose_name= _('مالیات')
    )
    total_payment = models.PositiveIntegerField(
        verbose_name= _('مبلغ قابل پرداخت')
    )
    status = models.CharField(
        max_length= 50,
        choices= (
            ('pending', _('در انتظار پرداخت')),
            ('paid', _('پرداخت شده')),
            ('canceled', _('لغو شده')),
        ),
        default = 'pending'
    )
    expires_at = models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= _('زمان انقضای پرداخت'),
    )
    sold_area = models.DecimalField(
        max_digits=14,
        decimal_places=6,
        default=0,
        verbose_name= _('متراژ فروخته شده'),
    )
    locked_area = models.DecimalField(
        max_digits=14,
        decimal_places=6,
        default=0,
        help_text= _("متراژی که در sale های فعال قفل شده")
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
        verbose_name = _("سرمایه‌گذاری")
        verbose_name_plural = _("سرمایه‌گذاری‌ها")



    def __str__(self):
        return (f"{self.user.fullname if self.user else '-'} | {self.project.title if self.project else '-'} |"
                f" {self.area} | {self.status}")




class InvestmentSale(AbstractDateTimeModel):

    investment = models.ForeignKey(
        Investment,
        on_delete= models.PROTECT,
        related_name= 'sales',
        verbose_name= _('سرمایه گذاری مرجع')
    )
    seller = models.ForeignKey(
        User,
        on_delete= models.PROTECT,
        related_name= 'sales',
        verbose_name= _('فروشنده')
    )
    buyer = models.ForeignKey(
        User,
        null= True,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name= _('خریدار'),
    )
    price_per_meter = models.PositiveIntegerField(
        verbose_name=  _('قیمت هر متر'),
    )
    selling_area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
        verbose_name= _('متراژ قابل فروش')
    )
    status = models.CharField(
        max_length= 50,
        choices= (
            ('selling',_('در انتظار فروش')),
            ('sold', _('فروخته شده')),
            ('canceled', _('کنسل شده')),
        ),
        default= 'selling'
    )
    sold_at = models.DateTimeField(
        null= True,
        blank= True,
        verbose_name= _('تاریخ فروش'),
    )
    # مبلغی که خریدار وارد میکنه (محاسبه متراژ و ... برعهده منه)
    base_amount = models.PositiveIntegerField(
        verbose_name= _('مبلغ خرید کاربر'),
    )
    sale_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name= _('انقضای فروش')
    )
    sold_area = models.DecimalField(
        max_digits= 14,
        decimal_places= 6,
        default= 0,
        verbose_name= _('متراژ فروخته شده'),
    )
    fee_amount = models.PositiveIntegerField(
        verbose_name= _('کارمزد')
    )
    tax_amount = models.PositiveIntegerField(
        verbose_name= _('مالیات')
    )
    total_payment = models.PositiveIntegerField(
        verbose_name= _('مبلغ قابل پرداخت')
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name= _('زمان انقضای پرداخت'),
    )
    is_featured = models.BooleanField(
        default= False,
        verbose_name= _("نمایش در صفحه اصلی")
    )


    def clean(self):
        if self.sold_area and self.selling_area:
            if self.sold_area > self.selling_area:
                raise ValidationError(_("متراژ فروخته شده نمی‌تواند از متراژ قابل فروش بیشتر باشد"))



    @property
    def remaining_area(self):
        return self.selling_area - self.sold_area


    @property
    def all_payment(self):
        return self.selling_area * self.price_per_meter

    @property
    def var_price(self):
        return self.investment.project.price_per_meter - self.price_per_meter


    class Meta:
        verbose_name = _("فروش سرمایه‌گذاری")
        verbose_name_plural = _("فروش سرمایه‌گذاری‌ها")

    def __str__(self):
        return f"{self.investment} | {self.seller}  | {self.status} "






