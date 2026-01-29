# Local Apps
from settings.models import SiteGlobalSetting, SocialMediaSetting
from .serializers import ContactUsMessageSerializer, SiteGlobalSettingSerializer, SocialMediaSettingSerializer

# Third Party Packages
from rest_framework import viewsets, status
from rest_framework.response import Response


class ContactUsViewSet(viewsets.ViewSet):
    """
    ViewSet ترکیبی برای صفحه Contact Us:
    - POST پیام جدید
    - GET اطلاعات سایت و شبکه‌های اجتماعی
    """

    # -----------------------------------
    # POST برا پیام جدید
    # -----------------------------------
    def create(self, request):
        serializer = ContactUsMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # -----------------------------------
    # GET برا اطلاعات سایت و شبکه‌ها
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
