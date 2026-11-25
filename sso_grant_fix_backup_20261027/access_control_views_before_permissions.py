from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ULBApplicationAccess, Role, Permission , RolePermission , UserApplicationAccess
from .serializers import (
    ULBApplicationAccessSerializer,
    RoleSerializer,
    PermissionSerializer,
    RolePermissionSerializer,
    UserApplicationAccessSerializer,
)


class ULBApplicationAccessViewSet(viewsets.ModelViewSet):

    queryset = (
        ULBApplicationAccess.objects
        .select_related('ulb', 'application')
        .all()
        .order_by('-created_at')
    )

    serializer_class = ULBApplicationAccessSerializer
    permission_classes = [IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):

    queryset = (
        Role.objects
        .select_related('application', 'ulb')
        .all()
        .order_by('role_name')
    )

    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]    

class PermissionViewSet(viewsets.ModelViewSet):

    queryset = Permission.objects.all().order_by('permission_name')

    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]    

class RolePermissionViewSet(viewsets.ModelViewSet):

    queryset = (
        RolePermission.objects
        .select_related('role', 'permission')
        .all()
        .order_by('role__role_name', 'permission__permission_name')
    )

    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]    

class UserApplicationAccessViewSet(viewsets.ModelViewSet):
    queryset = (
        UserApplicationAccess.objects
        .select_related(
            'user',
            'ulb',
            'application',
            'role',
        )
        .all()
        .order_by('-created_at')
    )

    serializer_class = UserApplicationAccessSerializer
    permission_classes = [IsAuthenticated]    