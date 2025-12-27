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

    # investment sale گرفتن quote
    path("investments/sale/quote/", views.InvestmentSaleQuoteAPIView.as_view(), name= "investment-sale-quote"),

    # investment sale (selling)
    path("investments/sale/create/", views.InvestmentSaleCreateAPIView.as_view(), name= "investment-sale-create"),

    # investment sale پرداخت
    path("investments/sale/<int:pk>/pay/", views.InvestmentSalePayAPIView.as_view(), name= "investment-sale-pay"),

    # investment sale cancel
    path("investments/sale/<int:pk>/cancel/", views.InvestmentSaleCancelAPIView.as_view(), name= "investment-sale-cancel"),

]
