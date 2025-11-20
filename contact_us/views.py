from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ContactUsMessages
from settings.models import SiteGlobalSetting, SocialMediaSetting
from .serializers import ContactUsMessageSerializer, SiteGlobalSettingSerializer, SocialMediaSettingSerializer

class ContactUsViewSet(viewsets.ViewSet):
    """
    ViewSet ترکیبی برای صفحه Contact Us:
    - POST پیام جدید
    - GET اطلاعات سایت و شبکه‌های اجتماعی
    """

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list_messages':
            return [permissions.IsAdminUser()]
        else:
            return [permissions.AllowAny()]

    # -----------------------------------
    # POST پیام جدید
    # -----------------------------------
    def create(self, request):
        serializer = ContactUsMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # -----------------------------------
    # GET اطلاعات سایت و شبکه‌ها
    # -----------------------------------
    def list(self, request):
        site_settings = SiteGlobalSetting.objects.first()
        social_media = SocialMediaSetting.objects.all()

        site_serializer = SiteGlobalSettingSerializer(site_settings)
        social_serializer = SocialMediaSettingSerializer(social_media, many=True)

        return Response({
            "site_global": site_serializer.data,
            "social_media": social_serializer.data
        })

    # -----------------------------------
    # GET تمام پیام‌ها برای ادمین
    # -----------------------------------
    @action(detail=False, methods=['get'], url_path='messages', url_name='messages')
    def list_messages(self, request):
        messages = ContactUsMessages.objects.all().order_by('-created')
        serializer = ContactUsMessageSerializer(messages, many=True)
        return Response(serializer.data)
