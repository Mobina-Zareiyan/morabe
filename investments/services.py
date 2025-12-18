from django.db import transaction
from rest_framework.exceptions import ValidationError
from settings.models import SiteGlobalSetting
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN
from account.models import UserWallet
from project.models import Project
from .models import Investment


def get_investment_expire_datetime():
    setting = SiteGlobalSetting.objects.first()
    if not setting:
        raise ValidationError("تنظیمات سایت یافت نشد")

    minutes = setting.investment_pending_expire_minutes
    return timezone.now() + timedelta(minutes=minutes)



@transaction.atomic
def pay_investment(investment):
    # الان سیستم کاملا ضد race شد
    investment = Investment.objects.select_for_update().get(pk=investment.pk)
    project = Project.objects.select_for_update().get(pk=investment.project_id)
    wallet = UserWallet.objects.select_for_update().get(user=investment.user)

    if investment.status != "pending":
        raise ValidationError("این سفارش قبلاً تعیین وضعیت شده است")

    if wallet.balance < investment.total_payment:
        raise ValidationError("موجودی کیف پول کافی نیست")

    if investment.expires_at and investment.expires_at < timezone.now():
        investment.status = "canceled"
        investment.save(update_fields=["status"])
        raise ValidationError("مهلت پرداخت این سفارش به پایان رسیده است")

    if project.current_funding + investment.base_amount > project.total_budget:
        raise ValidationError("ظرفیت پروژه تکمیل شده است")

    wallet.balance -= investment.total_payment
    wallet.save()

    project.current_funding += investment.base_amount
    project.save()

    investment.status = "paid"
    investment.save()

    return investment


def calculate_investment_amounts(*, project, area):
    setting = SiteGlobalSetting.objects.first()
    if not setting:
        raise ValidationError("تنظیمات سایت یافت نشد")

    price_per_meter = project.price_per_meter

    base_amount = (
        Decimal(area) * Decimal(price_per_meter)
    ).quantize(Decimal("1"), rounding=ROUND_DOWN)

    fee_amount = (
        base_amount * Decimal(setting.fee_percent) / Decimal(100)
    ).quantize(Decimal("1"), rounding=ROUND_DOWN)

    tax_amount = (
        base_amount * Decimal(setting.tax_percent) / Decimal(100)
    ).quantize(Decimal("1"), rounding=ROUND_DOWN)

    total_payment = base_amount + fee_amount + tax_amount

    remaining_budget = project.total_budget - project.current_funding

    if base_amount > remaining_budget:
        max_allowed_area = (
            Decimal(remaining_budget) / Decimal(price_per_meter)
        ).quantize(Decimal("0.001"), rounding=ROUND_DOWN)

        raise ValidationError({
            "detail": "مبلغ وارد شده بیشتر از ظرفیت باقی‌مانده پروژه است",
            "remaining_budget": remaining_budget,
            "entered_amount": base_amount,
            "max_allowed_amount": remaining_budget,
            "max_allowed_area": max_allowed_area,
        })

    return {
        "price_per_meter": price_per_meter,
        "base_amount": int(base_amount),
        "fee_amount": int(fee_amount),
        "tax_amount": int(tax_amount),
        "total_payment": int(total_payment),
    }