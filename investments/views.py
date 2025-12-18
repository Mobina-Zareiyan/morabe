# Django Module
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

# Local Module
from .models import Investment
from .serializers import InvestmentQuoteSerializer, InvestmentCreateSerializer
from .services import pay_investment




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
            "detail": "پرداخت با موفقیت انجام شد"
        })





