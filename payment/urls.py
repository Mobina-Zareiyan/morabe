# Django Built-in Modules
from django.urls import path

# Local Apps
from . import views


app_name = 'payment'

urlpatterns = [
    # موجودی
    path("wallet/", views.WalletDetailAPIView.as_view(), name="wallet-detail"),

    # برداشت
    path('withdrawal/create/', views.WithdrawRequestCreateAPIView.as_view(), name="withdrawal-create"),
    path('withdrawal/', views.WithdrawRequestListAPIView.as_view(), name="withdrawal-list"),
    path('withdrawal/approved/<int:pk>/', views.ApproveWithdrawRequestView.as_view(), name="approve-withdrawal"),
    path('withdrawal/reject/<int:pk>/', views.RejectWithdrawRequestView.as_view(), name="reject-withdrawal"),

    # تراکنش ها
    path("transaction/", views.TransactionAPIView.as_view(), name= 'transaction-list'),

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

