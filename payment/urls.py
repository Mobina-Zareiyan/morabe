from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # موجودی
    path("wallet/", views.WalletDetailAPIView.as_view(), name="wallet-detail"),

    # برداشت
    path('withdrawal/create/', views.WithdrawRequestCreateAPIView.as_view(), name="withdrawal-create"),
    path('withdrawal/', views.WithdrawRequestListAPIView.as_view(), name="withdrawal-list"),

    # پرداخت کیف پول
    path('deposit/create/', views.WalletDepositRequestAPIView.as_view(), name="deposit-create"),
    path('deposit/verify/', views.WalletDepositVerifyAPIView.as_view(), name="deposit-verify"),

    # مبلغ‌های پیشنهادی
    path('suggested-amounts/', views.SuggestedDepositAmountsAPIView.as_view(), name="suggested-amounts"),

    # کارت‌های بانکی
    path("cards/", views.CreditCardListAPIView.as_view(), name="card-list"),
    path("cards/create/", views.CreditCardCreateAPIView.as_view(), name="card-create"),
    path("cards/<int:pk>/delete/", views.CreditCardDeleteAPIView.as_view(), name="card-delete"),

]

