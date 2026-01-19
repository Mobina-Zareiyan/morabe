# Django Module
from django.utils import translation
# Local Module
from payment.models import WithdrawRequest

def setting(request):
    withdraw_requests = WithdrawRequest.objects.all()

    return {
        'withdraw_requests': withdraw_requests,
    }
