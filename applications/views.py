from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from access_control.permissions import IsSuperAdmin
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by(
        'display_order',
        'id',
    )
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsSuperAdmin()]