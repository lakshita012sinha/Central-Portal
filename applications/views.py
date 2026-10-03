from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('display_order', 'id')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]