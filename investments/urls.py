from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    # گرفتن quote برای یک پروژه
    path("investments/quote/", views.InvestmentQuoteAPIView.as_view(), name="investment-quote"),

    # ایجاد investment (pending)
    path("investments/create/", views.InvestmentCreateAPIView.as_view(), name="investment-create"),

    # پرداخت investment
    path("investments/<int:pk>/pay/", views.InvestmentPayAPIView.as_view(), name="investment-pay"),
]
