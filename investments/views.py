# Django Module
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


# Third Party Module
from decimal import Decimal

# Local Module
from .models import Investment, InvestmentSale
from .serializers import (InvestmentQuoteSerializer, InvestmentCreateSerializer,
                          InvestmentSaleQuoteSerializer, InvestmentSaleCreateSerializer,
                          InvestmentDetailSerializer, InvestmentSaleDetailSerializer)

from .services import pay_investment, pay_investment_sale, cancel_investment_sale




class InvestmentQuoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvestmentQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)




class InvestmentCreateAPIView(generics.CreateAPIView):
    serializer_class = InvestmentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}





class InvestmentPayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        investment = get_object_or_404(
            Investment,
            pk=pk,
            user=request.user
        )

        pay_investment(investment)

        return Response({
            "detail": _("پرداخت با موفقیت انجام شد")
        })

# این درسته؟؟؟
class InvestmentDetailAPIVew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        serializer = InvestmentDetailSerializer(many= True)
        return Response(serializer.data)


class InvestmentSaleQuoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvestmentSaleQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)



class InvestmentSaleCreateAPIView(generics.CreateAPIView):
    serializer_class = InvestmentSaleCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}




class InvestmentSalePayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sale = get_object_or_404(InvestmentSale, pk=pk, status="selling")
        purchase_area = Decimal(request.data.get("purchase_area"))

        pay_investment_sale(sale, buyer=request.user, purchase_area=purchase_area)

        return Response({"detail": _("پرداخت با موفقیت انجام شد")})







class InvestmentSaleCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

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


#   این درسته؟؟؟
class InvestmentSaleDetailAPIview(generics.ListAPIView):

    queryset = InvestmentSale.objects.all()
    serializer_class = InvestmentSaleDetailSerializer



