# Local Apps
from .models import ContactUsMessages
from settings.models import SiteGlobalSetting, SocialMediaSetting

# Third Party Packages
from rest_framework import serializers


# ----------------------------------------
# Serializer برای پیام‌های فرم Contact Us
# ----------------------------------------
class ContactUsMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsMessages
        fields = ['id', 'full_name', 'email', 'phone', 'message', 'is_checked', 'created']


# ----------------------------------------
# Serializer برای تنظیمات سایت
# ----------------------------------------
class SiteGlobalSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteGlobalSetting
        fields = ['address', 'map', 'email', 'phone']


# ----------------------------------------
# Serializer برای شبکه‌های اجتماعی
# ----------------------------------------
class SocialMediaSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSetting
        fields = ['name', 'username_or_id', 'icon', 'link']


# ----------------------------------------
# Serializer جامع برای صفحه Contact Us
# ----------------------------------------
class ContactUsPageDataSerializer(serializers.Serializer):
    site_global = SiteGlobalSettingSerializer(read_only=True)
    social_media = SocialMediaSettingSerializer(many=True, read_only=True)
