from django.db import transaction as db_transaction
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import Transaction, WithdrawRequest, CreditCard, Wallet


@db_transaction.atomic
def charge_wallet(wallet, amount, ref_id):
    wallet.balance += amount
    wallet.save()

    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=Transaction.DEPOSIT,
        status=Transaction.SUCCESS,
        reference_id=ref_id
    )




@db_transaction.atomic
def request_withdraw(wallet, bank_card, amount):

    if wallet.balance < amount:
        raise ValueError("Insufficient balance")

    wallet.balance -= amount
    wallet.save()

    withdraw = WithdrawRequest.objects.create(
        wallet=wallet,
        bank_card=bank_card,
        amount=amount
    )

    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=Transaction.WITHDRAW,
        status=Transaction.PENDING
    )

    return withdraw







def create_withdraw_request(user, bank_card_id, amount):
    wallet = user.wallet
    bank_card = CreditCard.objects.get(id=bank_card_id, user=user)

    if amount > wallet.available_balance:
        raise ValueError(_("موجودی کافی نیست"))

    with transaction.atomic():
        # بلوکه کردن موجودی
        wallet.blocked_balance += amount
        wallet.save()

        # ایجاد درخواست برداشت
        withdraw_request = WithdrawRequest.objects.create(
            wallet=wallet,
            bank_card=bank_card,
            amount=amount,
            status=WithdrawRequest.PENDING
        )

    return withdraw_request


def approve_withdraw_request(withdraw_request):
    wallet = withdraw_request.wallet

    with transaction.atomic():
        if withdraw_request.status != WithdrawRequest.PENDING:
            raise ValueError(_("این درخواست قابل تایید نیست."))

        # کم کردن موجودی واقعی و بلوکه
        wallet.balance -= withdraw_request.amount
        wallet.blocked_balance -= withdraw_request.amount
        wallet.save()

        withdraw_request.status = WithdrawRequest.APPROVED
        withdraw_request.reviewed_at = withdraw_request.now()
        withdraw_request.save()


def reject_withdraw_request(withdraw_request):
    wallet = withdraw_request.wallet

    with transaction.atomic():
        if withdraw_request.status != WithdrawRequest.PENDING:
            raise ValueError(_("این درخواست قابل رد کردن نیست."))

        # آزاد کردن مبلغ بلوکه شده
        wallet.blocked_balance -= withdraw_request.amount
        wallet.save()

        withdraw_request.status = WithdrawRequest.REJECTED
        withdraw_request.reviewed_at = withdraw_request.now()
        withdraw_request.save()
