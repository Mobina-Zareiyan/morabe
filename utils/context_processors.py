# Django Built-in Modules
from django.utils import translation

# Local Apps
from payment.models import WithdrawRequest


def setting(request):
    withdraw_requests = WithdrawRequest.objects.all()

    return {
        'withdraw_requests': withdraw_requests,
    }
