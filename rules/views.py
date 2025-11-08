from rest_framework import viewsets
from .models import Rules
from .serializers import RulesSerializer

class RulesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    فقط نمایش قوانین برای فرانت (GET)
    """
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer


