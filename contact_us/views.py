# Local Apps
from settings.models import SiteGlobalSetting, SocialMediaSetting
from .serializers import ContactUsMessageSerializer, ContactUsPageDataSerializer

# Third Party Packages
from rest_framework.response import Response
from rest_framework import generics



class ContactUsMessageAPIView(generics.CreateAPIView):
    serializer_class = ContactUsMessageSerializer


class ContactUsPageDetail(generics.GenericAPIView):
    serializer_class = ContactUsPageDataSerializer

    def get(self, request):
        site_settings = SiteGlobalSetting.objects.first()
        social_media = SocialMediaSetting.objects.all()

        data = {
            "site_settings": site_settings,
            "social_media": social_media
        }

        serializer = self.get_serializer(data)
        return Response (serializer.data)
