# Django Built-in Modules
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

# Local Apps
from account.models import User
from utils.models import AbstractDateTimeModel



class Wallet(AbstractDateTimeModel):
    user = models.OneToOneField(
        User,
        related_name="wallet",
        on_delete=models.PROTECT,
        verbose_name= _("کاربر")
    )
    balance = models.BigIntegerField(
        default=0,
        verbose_name= _("موجودی کل"),
        help_text = _("تومان"),
    )
    blocked_balance = models.BigIntegerField(
        default=0,
        verbose_name= _("موجودی بلوکه شده"),
        help_text=_("تومان"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name= _("فعال")
    )

    @property
    def available_balance(self):
        """موجودی قابل خرج کردن"""
        return self.balance - self.blocked_balance

    class Meta:
        verbose_name = _("کیف پول")
        verbose_name_plural = _("کیف پول ها")



    def __str__(self):
        return f"{self.user.fullname} - {self.balance} تومان"


class CreditCard(AbstractDateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="credit_cards",
        verbose_name= _("کاربر"),
    )
    sheba_number = models.CharField(
        max_length=26,
        verbose_name= _("شماره شبا"),
    )
    card_number = models.CharField(
        max_length=16,
        verbose_name= _("شماره کارت"),
    )
    bank_name = models.CharField(
        max_length=50,
        verbose_name= _("نام بانک")
    )
    is_active = models.BooleanField(
        default= True,
        verbose_name= _("فعال"),
    )


    class Meta:
        verbose_name = _("کارت اعتباری")
        verbose_name_plural = _("کارت های اعتباری")


    def __str__(self):
        return f"{self.bank_name} - {self.card_number[-4:]}"


class Transaction(AbstractDateTimeModel):

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    PURCHASE = "purchase"

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
        (PURCHASE, "Purchase"),
    ]

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        verbose_name= _("کیف پول"),
    )
    amount = models.BigIntegerField(
        verbose_name= _("مقدار")
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name= _("نوع تراکنش")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name= _("وضعیت تراکنش")
    )
    reference_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name= _("کد مرجع")
    )
    authority = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = _("تراکنش")
        verbose_name_plural = _("تراکنش ها")

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class WithdrawRequest(AbstractDateTimeModel):

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        verbose_name= _("کیف پول"),
    )
    bank_card = models.ForeignKey(
        CreditCard,
        on_delete=models.PROTECT,
        verbose_name= _("کارت مقصد")
    )
    amount = models.BigIntegerField(
        verbose_name= _("مبلغ برداشت")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name= _("وضعیت")
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name= _("زمان بررسی")
    )


    class Meta:
        verbose_name = _("درخواست برداشت")
        verbose_name_plural = _("درخواست های برداشت")

    def __str__(self):
        return f"{self.wallet.user} - {self.amount}"






class SuggestedDepositAmount(AbstractDateTimeModel):
    amount = models.PositiveBigIntegerField(
        verbose_name= _("مبلغ پیشنهادی"),
        help_text= _("تومان"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name= _("فعال")
    )

    class Meta:
        verbose_name = _("مبلغ پیشنهادی")
        verbose_name_plural = _("مبلغ‌های پیشنهادی")
        ordering = ['amount']

    def __str__(self):
        return f"{self.amount} تومان"










