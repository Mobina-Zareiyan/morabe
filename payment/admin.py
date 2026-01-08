from django.contrib import admin
from .models import Wallet, CreditCard, Transaction, WithdrawRequest, SuggestedDepositAmount
from utils.admin import DateTimeAdminMixin



# ---------------------------
# Wallet Admin
# ---------------------------
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "balance",
        "blocked_balance",
        "available_balance",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("user__fullname",)
    readonly_fields = (
        "balance",
        "blocked_balance",
        "available_balance",
        "user",
        *DateTimeAdminMixin.readonly_fields,
    )


# ---------------------------
# CreditCard Admin
# ---------------------------
@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bank_name",
        "card_number",
        "sheba_number",
        "is_active",
    )
    list_filter = ("is_active", "bank_name")
    search_fields = ("user__fullname", "card_number", "sheba_number", "bank_name")
    readonly_fields = ( *DateTimeAdminMixin.readonly_fields,)


# ---------------------------
# Transaction Admin
# ---------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "transaction_type",
        "amount",
        "status",
        "reference_id",
        "authority",
    )
    list_filter = ("transaction_type", "status")
    search_fields = ("wallet__user__fullname", "authority", "reference_id")
    readonly_fields = (
        "wallet",
        "transaction_type",
        "amount",
        "status",
        "reference_id",
        "authority",
        *DateTimeAdminMixin.readonly_fields,
    )


# ---------------------------
# WithdrawRequest Admin
# ---------------------------
@admin.register(WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount",
        "bank_card",
        "status",
        "reviewed_at",
    )
    list_filter = ("status",)
    search_fields = ("wallet__user__fullname", "bank_card__card_number", "bank_card__sheba_number")
    readonly_fields = (
        "wallet",
        "bank_card",
        "amount",
        *DateTimeAdminMixin.readonly_fields,
    )


# ---------------------------
# SuggestedDepositAmount Admin
# ---------------------------
@admin.register(SuggestedDepositAmount)
class SuggestedDepositAmountAdmin(admin.ModelAdmin):
    list_display = ("amount", "is_active")
    list_filter = ("is_active",)
    search_fields = ("amount",)
    # readonly_fields = ("created_at", "updated_at")
