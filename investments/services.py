# Django Module
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

# Third Party Module
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN
from settings.models import SiteGlobalSetting

# Local Module
from account.models import UserWallet
from project.models import Project
from .models import Investment , InvestmentSale
from account.models import User



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

    if investment.area > project.remaining_area:
        investment.status = "canceled"
        investment.save(update_fields=["status"])
        raise ValidationError("ظرفیت متراژی پروژه تکمیل شده است")

    wallet.balance -= investment.total_payment
    wallet.save()

    project.current_funding += investment.base_amount
    project.save()

    investment.status = "paid"
    investment.save()



    return investment



def get_project_pending_area(project):
    return (
        Investment.objects
        .filter(project=project, status="pending")
        .aggregate(total=Sum("area"))["total"]
        or Decimal("0")
    )


def get_project_remaining_area_for_quote(project):
    return project.investable_area - project.sold_area - get_project_pending_area(project)



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

    real_remaining_area = project.investable_area - project.sold_area
    quote_remaining_area = get_project_remaining_area_for_quote(project)

    if area > quote_remaining_area:
        if real_remaining_area <= 0:
            raise ValidationError({
                "detail": "ظرفیت پروژه تکمیل شده است"
            })
        else:
            raise ValidationError({
                "detail": "ظرفیت پروژه به‌صورت موقت رزرو شده است. لطفاً دقایقی بعد دوباره تلاش کنید.",
                "remaining_area": quote_remaining_area,
                "entered_area": area,
                "max_allowed_area": quote_remaining_area
            })

    return {
        "price_per_meter": int(price_per_meter),
        "base_amount": int(base_amount),
        "fee_amount": int(fee_amount),
        "tax_amount": int(tax_amount),
        "total_payment": int(total_payment),
    }




def calculate_investment_by_amount(*, investment, base_amount):
    setting = SiteGlobalSetting.objects.first()
    if not setting:
        raise ValidationError("تنظیمات سایت یافت نشد")

    base_amount = Decimal(base_amount)
    price_per_meter = Decimal(investment.price_per_meter)

    area = (base_amount / price_per_meter).quantize(
        Decimal("0.000001"), rounding=ROUND_DOWN
    )

    if area <= 0:
        raise ValidationError("مبلغ وارد شده معتبر نیست")

    sellable_area = investment.remaining_area

    if area > sellable_area:
        raise ValidationError({
            "detail": "مبلغ وارد شده بیشتر از دارایی فروشنده است",
            "sellable_area": sellable_area,
            "entered_area": area,
        })

    fee_amount = (
            base_amount * Decimal(setting.fee_percent) / 100
    ).quantize(Decimal("1"), rounding=ROUND_DOWN)

    tax_amount = (
            base_amount * Decimal(setting.tax_percent) / 100
    ).quantize(Decimal("1"), rounding=ROUND_DOWN)

    total_payment = base_amount + fee_amount + tax_amount

    return {
        "area": area,
        "price_per_meter": int(price_per_meter),
        "base_amount": int(base_amount),
        "fee_amount": int(fee_amount),
        "tax_amount": int(tax_amount),
        "total_payment": int(total_payment),
    }



@transaction.atomic
def create_investment_sale(*, seller, investment, amounts):
    investment = Investment.objects.select_for_update().get(pk=investment.pk)

    if investment.status != "paid":
        raise ValidationError("سرمایه‌گذاری قابل فروش نیست")

    if amounts["area"] > investment.remaining_area:
        raise ValidationError("دارایی قابل فروش کافی نیست")

    investment.locked_area += amounts["area"]
    investment.save(update_fields=["locked_area"])

    return InvestmentSale.objects.create(
        seller=seller,
        investment=investment,
        selling_area=amounts["area"],
        price_per_meter=amounts["price_per_meter"],
        base_amount=amounts["base_amount"],
        fee_amount=amounts["fee_amount"],
        tax_amount=amounts["tax_amount"],
        total_payment=amounts["total_payment"],
        status="selling",
        expires_at=get_investment_expire_datetime()
    )



@transaction.atomic
def pay_investment_sale(sale: InvestmentSale, buyer: User, purchase_area: Decimal):
    # 1. Lock همه چیز مهم
    sale = InvestmentSale.objects.select_for_update().get(pk=sale.pk)
    investment = Investment.objects.select_for_update().get(pk=sale.investment_id)

    buyer_wallet = UserWallet.objects.select_for_update().get(user=buyer)
    seller_wallet = UserWallet.objects.select_for_update().get(user=sale.seller)

    # 2. اعتبارسنجی
    if sale.status != "selling":
        raise ValidationError("این آگهی فعال نیست")

    if purchase_area <= 0:
        raise ValidationError("متراژ نامعتبر است")

    if purchase_area > sale.remaining_area:
        raise ValidationError("متراژ درخواستی بیشتر از مقدار قابل فروش است")

    if purchase_area > investment.remaining_area:
        raise ValidationError("دارایی فروشنده کافی نیست")


    # 3. محاسبات مالی
    base_amount = (purchase_area * Decimal(sale.price_per_meter)).quantize(
        Decimal("1"), rounding=ROUND_DOWN
    )

    setting = SiteGlobalSetting.objects.first()
    fee_amount = (base_amount * Decimal(setting.fee_percent) / 100).quantize(
        Decimal("1"), rounding=ROUND_DOWN
    )
    tax_amount = (base_amount * Decimal(setting.tax_percent) / 100).quantize(
        Decimal("1"), rounding=ROUND_DOWN
    )

    total_payment = base_amount + fee_amount + tax_amount

    if buyer_wallet.balance < total_payment:
        raise ValidationError("موجودی کیف پول خریدار کافی نیست")

    # 4. انتقال پول
    buyer_wallet.balance -= total_payment
    buyer_wallet.save(update_fields=["balance"])

    seller_wallet.balance += base_amount
    seller_wallet.save(update_fields=["balance"])

    # (fee + tax اینجا می‌تواند به کیف پول سیستم برود)

    # 5. آپدیت Sale
    sale.sold_area += purchase_area


    if sale.remaining_area == 0:
        sale.status = "sold"

    sale.save()

    # 6. کاهش دارایی seller
    investment.sold_area += purchase_area
    investment.locked_area -= purchase_area
    investment.save(update_fields=["sold_area", "locked_area"])

    assert investment.sold_area >= 0
    assert investment.locked_area >= 0
    assert investment.sold_area + investment.locked_area <= investment.area

    # 7. ساخت دارایی جدید برای buyer
    Investment.objects.create(
        user=buyer,
        project=investment.project,
        area=purchase_area,
        price_per_meter=sale.price_per_meter,
        base_amount=int(base_amount),
        fee_amount=int(fee_amount),
        tax_amount=int(tax_amount),
        total_payment=int(total_payment),
        status="paid",
        expires_at=None
    )

    return sale




@transaction.atomic
def cancel_investment_sale(sale: InvestmentSale):
    """
    لغو فروش سرمایه‌گذاری قبل از اینکه خریدار مبلغ را پرداخت کند.
    فقط فروش‌های در حال انتظار (selling) قابل لغو هستند.
    """
    # 1. قفل رکوردها برای جلوگیری از race condition
    sale = InvestmentSale.objects.select_for_update().get(pk=sale.pk)
    investment = Investment.objects.select_for_update().get(pk=sale.investment_id)
    seller_wallet = UserWallet.objects.select_for_update().get(user=sale.seller)

    # 2. بررسی وضعیت sale
    if sale.status != "selling":
        raise ValidationError("فروش فقط در وضعیت در انتظار فروش قابل لغو است")

    # 3. بازگرداندن locked_area به investment
    investment.locked_area -= sale.selling_area
    if investment.locked_area < 0:
        raise ValidationError("خطا در محاسبه متراژ قفل شده")
    investment.save(update_fields=["locked_area"])

    # 4. وضعیت sale را لغو می‌کنیم
    sale.status = "canceled"
    sale.save(update_fields=["status"])


    return sale











