# Django built-in  Modules
from rest_framework import serializers

# Local Modules
from project.models import Project
from .models import Investment
from .services import get_investment_expire_datetime, calculate_investment_amounts



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
        )






