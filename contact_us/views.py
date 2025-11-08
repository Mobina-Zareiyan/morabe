from rest_framework import viewsets, permissions
from .models import ContactUsMessages
from .serializers import ContactUsMessageSerializer

class ContactUsMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت پیام‌های فرم Contact Us
    کاربران می‌توانند پیام جدید ارسال کنند (POST)
    ادمین می‌تواند پیام‌ها را مشاهده و بررسی کند
    """
    queryset = ContactUsMessages.objects.all().order_by('-created')
    serializer_class = ContactUsMessageSerializer

    # دسترسی‌ها:
    # کاربران فقط می‌تونن POST کنن و پیام‌ها رو ببینن.
    # ادمین می‌تونه همه عملیات رو انجام بده.

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']: #عملیات درحال اجرا

            permission_classes = [permissions.IsAdminUser]
        else:
            # بقیه عملیات (create) برای همه بازه
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes] # یه instance میسازه و ارسالش مکنه.
