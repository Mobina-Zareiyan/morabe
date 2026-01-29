# Django Built-in Modules
from rest_framework import serializers

# Local Apps
from .models import CreditCard, SuggestedDepositAmount, Wallet, Transaction, WithdrawRequest

# Third Party Packages
from django.utils.translation import gettext_lazy as _


class WithdrawRequestSerializer(serializers.Serializer):
    bank_card_id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)

    def validate_bank_card_id(self, value):
        user = self.context['request'].user
        if not CreditCard.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError(_("کارت انتخاب شده معتبر نیست."))
        return value

    def validate_amount(self, value):
        wallet = self.context['request'].user.wallet
        if value > wallet.available_balance:
            raise serializers.ValidationError(_("موجودی کافی برای برداشت ندارید."))
        return value


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("مبلغ باید بزرگتر از صفر باشد."))
        return value




class SuggestedDepositAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedDepositAmount
        fields = ['id', 'amount']






class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = (
            "id",
            "sheba_number",
            "card_number",
            "bank_name",
        )

    def validate_card_number(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError(_("شماره کارت باید ۱۶ رقم باشد."))
        return value

    def validate_sheba_number(self, value):
        if not value.startswith("IR") or len(value) != 26:
            raise serializers.ValidationError(_("شماره شبا معتبر نیست."))
        return value





class WalletSerializer(serializers.ModelSerializer):
    available_balance = serializers.IntegerField(read_only=True)
    user_fullname = serializers.CharField(source="user.fullname", read_only=True)

    class Meta:
        model = Wallet
        fields = ["user_fullname", "balance", "blocked_balance", "available_balance"]


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["amount", "transaction_type", "status", "created", "wallet"]



class WithdrawApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = ["wallet", "bank_card", "amount", "status"]



# class WithdrawRequestPendingSerializer(serializers.Serializer):







