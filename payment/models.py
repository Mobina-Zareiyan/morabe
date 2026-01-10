from django.db import models, transaction
from account.models import User
from utils.models import AbstractDateTimeModel


class Wallet(AbstractDateTimeModel):
    user = models.OneToOneField(
        User,
        related_name="wallet",
        on_delete=models.PROTECT,
        verbose_name="کاربر"
    )
    balance = models.BigIntegerField(
        default=0,
        verbose_name="موجودی کل"
    )
    blocked_balance = models.BigIntegerField(
        default=0,
        verbose_name="موجودی بلوکه شده"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    @property
    def available_balance(self):
        """موجودی قابل خرج کردن"""
        return self.balance - self.blocked_balance

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول ها"



    def __str__(self):
        return f"{self.user.fullname} - {self.balance} تومان"


class CreditCard(AbstractDateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="credit_cards",
        verbose_name="کاربر",
    )
    sheba_number = models.CharField(
        max_length=26,
        verbose_name="شماره شبا",
    )
    card_number = models.CharField(
        max_length=16,
        verbose_name="شماره کارت",
    )
    bank_name = models.CharField(
        max_length=50,
        verbose_name="نام بانک"
    )
    is_active = models.BooleanField(
        default= True,
        verbose_name= "فعال",
    )


    class Meta:
        verbose_name = "کارت اعتباری"
        verbose_name_plural = "کارت های اعتباری"


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
        verbose_name="کیف پول",
    )
    amount = models.BigIntegerField(verbose_name="مقدار")
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="نوع تراکنش"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name="وضعیت تراکنش"
    )
    reference_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="کد مرجع"
    )
    authority = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش ها"

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
        verbose_name="کیف پول",
    )
    bank_card = models.ForeignKey(
        CreditCard,
        on_delete=models.PROTECT,
        verbose_name="کارت مقصد"
    )
    amount = models.BigIntegerField(verbose_name="مبلغ برداشت")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name="وضعیت"
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان بررسی"
    )


    class Meta:
        verbose_name = "درخواست برداشت"
        verbose_name_plural = "درخواست های برداشت"

    def __str__(self):
        return f"{self.wallet.user} - {self.amount}"






class SuggestedDepositAmount(AbstractDateTimeModel):
    amount = models.PositiveBigIntegerField(
        verbose_name="مبلغ پیشنهادی",
        help_text= "تومان",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    class Meta:
        verbose_name = "مبلغ پیشنهادی"
        verbose_name_plural = "مبلغ‌های پیشنهادی"
        ordering = ['amount']

    def __str__(self):
        return f"{self.amount} تومان"










