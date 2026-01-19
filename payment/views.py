# Django Module
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db import transaction
from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _


# Local Module
from .serializers import (WithdrawRequestSerializer, DepositSerializer,
                          SuggestedDepositAmountSerializer, CreditCardSerializer, WalletSerializer,
                          TransactionSerializer)
from .services import create_withdraw_request, reject_withdraw_request, approve_withdraw_request
from .models import WithdrawRequest, Transaction, SuggestedDepositAmount, CreditCard, Wallet
from morabe import settings





ZARINPAL_REQUEST_URL = settings.ZARINPAL_REQUEST_URL
ZARINPAL_START_PAY_URL = settings.ZARINPAL_START_PAY_URL
ZARINPAL_VERIFY_URL = settings.ZARINPAL_VERIFY_URL




# ---------------------------
# 1. ثبت درخواست برداشت
# ---------------------------
class WithdrawRequestCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        withdraw_request = create_withdraw_request(
            user=request.user,
            bank_card_id=serializer.validated_data['bank_card_id'],
            amount=serializer.validated_data['amount']
        )

        return Response(
            {
                "message": _("درخواست برداشت با موفقیت ثبت شد"),
                "withdraw_request_id": withdraw_request.id,
                "available_balance": request.user.wallet.available_balance
            },
            status=status.HTTP_201_CREATED
        )



# ---------------------------
# 2. مشاهده درخواست‌های خود کاربر
# ---------------------------
class WithdrawRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet
        requests = WithdrawRequest.objects.filter(wallet=wallet).order_by('-created_at')

        data = [
            {
                "id": r.id,
                "amount": r.amount,
                "status": r.status,
                "bank_card": f"{r.bank_card.bank_name} - {r.bank_card.card_number[-4:]}",
                "created_at": r.created,
                "reviewed_at": r.reviewed_at
            }
            for r in requests
        ]

        return Response(data)





# ---------------------------
# 3. اتصال به درگاه رپداخت
# ---------------------------

class WalletDepositRequestAPIView(APIView):
    """
    ایجاد درخواست پرداخت و هدایت به درگاه زرین‌پال.
    این ویو:
    - مبلغ‌های پیشنهادی فعال را می‌پذیرد
    - یا مبلغ‌های دستی معتبر (>0)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        mobile = request.user.mobile_number
        wallet = request.user.wallet

        # بررسی مبلغ
        if amount <= 0:
            return Response(
                {"error": _("مبلغ باید بزرگتر از صفر باشد.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # بررسی اگر مبلغ از بین پیشنهادهای فعال باشد
        valid_suggested = SuggestedDepositAmount.objects.filter(
            amount=amount, is_active=True
        ).exists()



        payload = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount,
            "currency": "IRT",
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
            "description": f"افزایش موجودی کیف پول کاربر {request.user.id}",
            "metadata": {
                "mobile": mobile,
                "user_id": request.user.id
            }
        }

        try:
            response = requests.post(ZARINPAL_REQUEST_URL, json=payload, timeout=10)
            result = response.json()
        except Exception as e:
            return Response(
                {"error": _("خطا در اتصال به درگاه پرداخت"), "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data = result.get("data", {})
        authority = data.get("authority")

        if authority:
            # ذخیره تراکنش در دیتابیس
            with db_transaction.atomic():
                Transaction.objects.create(
                    wallet=wallet,
                    amount=amount,
                    transaction_type=Transaction.DEPOSIT,
                    status=Transaction.PENDING,
                    authority=authority,
                    mobile=mobile
                )

            payment_url = f"{ZARINPAL_START_PAY_URL}{authority}"
            return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)

        return Response(
            {"error": _("خطا در ایجاد تراکنش"), "details": data.get("message")},
            status=status.HTTP_400_BAD_REQUEST
        )




# ---------------------------
# 4. افزایش موجودی کیف پول
# ---------------------------

class WalletDepositVerifyAPIView(APIView):
    """
    Callback زرین‌پال و تایید پرداخت
    """

    def get(self, request):
        authority = request.GET.get("Authority")
        status_param = request.GET.get("Status")

        if not authority or status_param != "OK":
            return Response(
                {"error": _("پرداخت توسط کاربر لغو شد.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transaction_record = Transaction.objects.select_for_update().get(
                authority=authority,
                status=Transaction.PENDING
            )
        except Transaction.DoesNotExist:
            return Response(
                {"error": _("تراکنش معتبر نیست یا قبلاً تایید شده است.")},
                status=status.HTTP_404_NOT_FOUND
            )

        payload = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": transaction_record.amount,
            "authority": authority
        }

        try:
            response = requests.post(ZARINPAL_VERIFY_URL, json=payload, timeout=10)
            result = response.json()
        except Exception as e:
            return Response(
                {"error": _("خطا در ارتباط با زرین‌پال"), "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data = result.get("data", {})

        if data.get("code") == 100:
            with transaction.atomic():
                transaction_record.status = Transaction.SUCCESS
                transaction_record.reference_id = data.get("reference_id")
                transaction_record.save()

                wallet = transaction_record.wallet
                wallet.balance += transaction_record.amount
                wallet.save()

            return Response({
                "message": _("پرداخت با موفقیت انجام شد."),
                "reference_id": transaction_record.reference_id,
                "new_balance": wallet.balance
            }, status=status.HTTP_200_OK)

        # اگر پرداخت ناموفق بود
        transaction_record.status = Transaction.FAILED
        transaction_record.save()

        return Response(
            {"error": _("پرداخت ناموفق بود."), "details": data.get("message")},
            status=status.HTTP_400_BAD_REQUEST
        )



# ---------------------------
# 5. ارسال میلغ های پیشنهادی به فرانت
# ---------------------------
class SuggestedDepositAmountsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        amounts = SuggestedDepositAmount.objects.filter(is_active=True)
        serializer = SuggestedDepositAmountSerializer(amounts, many=True)
        return Response(serializer.data)





# ---------------------------
# 6. افزودن کارت بانکی
# ---------------------------
class CreditCardCreateAPIView(APIView):
    """
    افزودن کارت بانکی جدید برای کاربر
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreditCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # جلوگیری از ثبت کارت تکراری برای یک کاربر
        if CreditCard.objects.filter(
            user=request.user,
            card_number=serializer.validated_data["card_number"]
        ).exists():
            return Response(
                {"error": _("این کارت قبلاً ثبت شده است.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        credit_card = serializer.save(user=request.user)

        return Response(
            {
                "message": _("کارت بانکی با موفقیت ثبت شد."),
                "card": CreditCardSerializer(credit_card).data
            },
            status=status.HTTP_201_CREATED
        )





# ---------------------------
# 7. نمایش تمامی کارت های بانکی
# ---------------------------

class CreditCardListAPIView(APIView):
    """
    لیست کارت‌های بانکی کاربر
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = CreditCard.objects.filter(user=request.user, is_active= True).order_by("-created_at")
        serializer = CreditCardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





# ---------------------------
# 8. حذف کارت (غیرفعال کردن)
# ---------------------------
class CreditCardDeleteAPIView(APIView):
    """
    حذف کارت بانکی با soft delete (is_active=False)
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            card = CreditCard.objects.get(pk=pk, user=request.user, is_active=True)
        except CreditCard.DoesNotExist:
            return Response(
                {"error": _("کارت پیدا نشد یا قبلاً حذف شده است.")},
                status=status.HTTP_404_NOT_FOUND
            )

        card.is_active = False
        card.save()

        return Response(
            {"message": _("کارت با موفقیت حذف شد.")},
            status=status.HTTP_200_OK
        )





# ---------------------------
# 9. نمایش کیف پول به کاربر
# ---------------------------

class WalletDetailAPIView(APIView):
    """
    مشاهده موجودی کیف پول کاربر
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wallet = request.user.wallet
        except Wallet.DoesNotExist:
            return Response(
                {"error": _("کیف پول یافت نشد.")},
                status=404
            )

        serializer = WalletSerializer(wallet)
        return Response(serializer.data)




# ---------------------------
# 10. نمایش تراکنش های کیف پول به کاربر
# ---------------------------
class TransactionAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(wallet__user= user)




# ---------------------------
# 11. قبول درخواست برداشت
# ---------------------------
class ApproveWithdrawRequestView(APIView):
    def post(self, request, pk):
        withdraw_request = WithdrawRequest.objects.get(pk=pk)
        approve_withdraw_request(withdraw_request)
        return Response(
            {
                "message": _("واریز به حساب کاربر با موفقیت به پایان رسید."),
                "withdraw_id": pk,
                "available_balance": withdraw_request.wallet.available_balance
            },
            status=status.HTTP_201_CREATED
        )


# ---------------------------
# 12. رد درخواست برداشت
# ---------------------------
class RejectWithdrawRequestView(APIView):
    def post(self, request, pk):
        withdraw_request = WithdrawRequest.objects.get(pk=pk)
        reject_withdraw_request(withdraw_request)
        return Response(
            {
                "message": _("درخواست واریز به حساب کاربر رد شد."),
                "withdraw_id": pk,
                "available_balance": withdraw_request.wallet.available_balance
            },
            status=status.HTTP_201_CREATED
        )













