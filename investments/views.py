# Django Module
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedUser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


# Third Party Module
from decimal import Decimal

# Local Module
from .models import Investment, InvestmentSale
from .serializers import (InvestmentQuoteSerializer, InvestmentCreateSerializer,
                          InvestmentSaleQuoteSerializer, InvestmentSaleCreateSerializer, CreateInvestmentSaleSerializer,
                          InvestmentDetailSerializer, InvestmentSaleDetailSerializer)

from .services import pay_investment, pay_investment_sale, cancel_investment_sale
from .domain import PaymentSuccess, CapacityExceeded, ExpiredInvestment




class InvestmentQuoteAPIView(APIView):
    serializer_class = InvestmentQuoteSerializer
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        serializer = InvestmentQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)




class InvestmentCreateAPIView(generics.CreateAPIView):
    serializer_class = InvestmentCreateSerializer
    permission_classes = [IsAuthenticatedUser]

    def get_serializer_context(self):
        return {"request": self.request}





class InvestmentPayAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, pk):
        investment = get_object_or_404(
            Investment,
            pk=pk,
            user=request.user
        )

        result = pay_investment(investment)

        if isinstance(result, ExpiredInvestment):
            raise ValidationError("مهلت پرداخت این سفارش به پایان رسیده است")

        if isinstance(result, CapacityExceeded):
            raise ValidationError(_("ظرفیت متراژی پروژه تکمیل شده است"))

        return Response({
            "detail": _("پرداخت با موفقیت انجام شد")
        })

# این درسته؟؟؟
class InvestmentDetailAPIVew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        serializer = InvestmentDetailSerializer(many= True)
        return Response(serializer.data)


class CreateInvestmentSaleAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        serializer = CreateInvestmentSaleSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)

        pass



class InvestmentSaleQuoteAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        serializer = InvestmentSaleQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)



class InvestmentSaleCreateAPIView(generics.CreateAPIView):
    serializer_class = InvestmentSaleCreateSerializer
    permission_classes = [IsAuthenticatedUser]

    def get_serializer_context(self):
        return {"request": self.request}




class InvestmentSalePayAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, pk):
        sale = get_object_or_404(InvestmentSale, pk=pk, status="selling")
        purchase_area = Decimal(request.data.get("purchase_area"))

        pay_investment_sale(sale, buyer=request.user, purchase_area=purchase_area)

        return Response({"detail": _("پرداخت با موفقیت انجام شد")})







class InvestmentSaleCancelAPIView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, pk):
        # دریافت sale و اطمینان از مالک بودن فروش
        sale = get_object_or_404(InvestmentSale, pk=pk, seller=request.user)

        # لغو sale با سرویس
        try:
            cancel_investment_sale(sale)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": _("فروش با موفقیت لغو شد")}
        )



class InvestmentSaleListAPIview(generics.ListAPIView):

    queryset = InvestmentSale.objects.filter(status= "selling")
    serializer_class = InvestmentSaleDetailSerializer





# #   این درسته؟؟؟ بقیه اطالاعاتش رو چجوری بهش اضافه کنم؟؟؟؟خدایا کاش من انقدر حالیم بود که باید چیکار کنم
# class InvestmentSaleListAPIview(generics.GenericAPIView):
#     serializer_class = InvestmentSaleDetailSerializer
#
#     def get(self, request):
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         var_price = serializer.validated_data['var_price']
#
#         if var_price < 0:
#             return Response(
#                 {
#                     'detail': "زیر قیمت بازار",
#                     "var_price": -1 * var_price,
#                  }
#             )
#
#         elif var_price > 0:
#             return Response(
#                 {
#                     'detail': "بالای قیمت بازار",
#                     "var_price": var_price
#                 }
#             )
#
#         else:
#             return Response(
#                 {
#                     'detail': "یکسان با قیمت بازار",
#                     "var_price": 0
#                 }
#             )
#



