# Local Apps
from .models import Rules
from .serializers import RulesSerializer

# Third Party Packages
from rest_framework import viewsets



class RulesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    فقط نمایش قوانین برای فرانت (GET)
    """
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer


