# Django built-in  Modules
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


# Local Modules
from project.models import Project
from .models import Investment, InvestmentSale
from .services import (get_investment_expire_datetime, calculate_investment_amounts,
                       calculate_investment_by_amount, create_investment_sale)



class InvestmentQuoteSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    area = serializers.DecimalField(max_digits=10, decimal_places=3)

    def validate(self, data):
        return calculate_investment_amounts(
            project=data["project"],
            area=data["area"]
        )


class InvestmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ("project", "area")

    def validate(self, attrs):
        project = attrs["project"]
        area = attrs["area"]

        # بررسی ظرفیت باقی‌مانده پروژه
        amounts = calculate_investment_amounts(project=project, area=area)
        if not amounts:
            raise serializers.ValidationError(_("مشکلی در محاسبات سرمایه‌گذاری پیش آمد"))
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        project = validated_data["project"]
        area = validated_data["area"]
        expires_at = get_investment_expire_datetime()

        amounts = calculate_investment_amounts(
            project=project,
            area=area
        )

        return Investment.objects.create(
            user=user,
            project=project,
            area=area,
            price_per_meter=amounts["price_per_meter"],
            base_amount=amounts["base_amount"],
            fee_amount=amounts["fee_amount"],
            tax_amount=amounts["tax_amount"],
            total_payment=amounts["total_payment"],
            status="pending",
            expires_at=expires_at
        )



class InvestmentDetailSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="project.title", read_only=True)

    class Meta:
        model = Investment
        fields = (
            "id",
            "project_title",
            "area",
            "price_per_meter",
            "base_amount",
            "fee_amount",
            "tax_amount",
            "total_payment",
            "status",
            "created",
            "sold_area",
            "locked_area",

        )



class InvestmentSaleQuoteSerializer(serializers.Serializer):
    investment = serializers.PrimaryKeyRelatedField(
        queryset=Investment.objects.filter(status="paid")
    )
    base_amount = serializers.IntegerField(min_value=1)

    def validate(self, data):
        return calculate_investment_by_amount(
            investment=data["investment"],
            base_amount=data["base_amount"]
        )




class InvestmentSaleCreateSerializer(serializers.ModelSerializer):
    investment = serializers.PrimaryKeyRelatedField(
        queryset=Investment.objects.filter(status="paid")
    )

    class Meta:
        model = InvestmentSale
        fields = ("investment", "base_amount")
    def validate(self, attrs):
        request = self.context["request"]
        investment = attrs["investment"]
        base_amount = attrs.get("base_amount")

        # 1. مالک بودن
        if investment.user != request.user:
            raise serializers.ValidationError(_("شما مالک این سرمایه‌گذاری نیستید"))

        # 2. وضعیت investment
        if investment.status != "paid":
            raise serializers.ValidationError(_("فقط سرمایه‌گذاری‌های پرداخت‌شده قابل فروش هستند"))

        # 3. دارایی قابل فروش
        if investment.remaining_area <= 0:
            raise serializers.ValidationError(_("دارایی قابل فروش وجود ندارد"))

        # 4. اعتبارسنجی base_amount
        amounts = calculate_investment_by_amount(
            investment=investment,
            base_amount=base_amount
        )

        if amounts["area"] > investment.remaining_area:
            raise serializers.ValidationError(_("مقدار وارد شده بیش از دارایی قابل فروش است"))

        # اضافه کردن مقادیر محاسبه‌شده به attrs برای create
        attrs.update(amounts)
        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        return create_investment_sale(
            seller=request.user,
            investment=validated_data["investment"],
            amounts=validated_data["_amounts"]
        )


class InvestmentSaleDetailSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="investment.project.title", read_only=True)
    remaining_area = serializers.DecimalField(max_digits= 14, decimal_places= 6, source= "remaining_area", read_only= True)
    all_payment = serializers.DecimalField(max_digits= 14, decimal_places= 6, source= "all_payment", read_only= True)
    var_price = serializers.DecimalField(max_digits= 14, decimal_places= 6, source= "var_price", read_only= True)

    class Meta:
        model = InvestmentSale
        fields = (
            "id",
            "project_title",
            "remaining_area",
            "price_per_meter",
            "all_payment",
            "status",
            "created",
            "is_featured",
            "var_price",
        )







