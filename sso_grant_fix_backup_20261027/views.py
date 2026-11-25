from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from access_control.permissions import IsSuperAdmin

from .models import ULB, ULBDatabaseConfiguration, ULBApplication
from .serializers import (
    ULBSerializer,
    ULBDatabaseConfigurationSerializer,
    ULBApplicationSerializer,
)


class ULBListCreateView(generics.ListCreateAPIView):
    """
    GET  — any authenticated user can list ULBs.
    POST — Super Admin only.
    """

    queryset = ULB.objects.all().order_by('ulb_name')
    serializer_class = ULBSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ULBDetailView(generics.RetrieveUpdateAPIView):
    """
    GET        — any authenticated user can retrieve a ULB.
    PUT/PATCH  — Super Admin only.
    """

    queryset = ULB.objects.all()
    serializer_class = ULBSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ULBDatabaseConfigListCreateView(generics.ListCreateAPIView):
    """
    GET  — any authenticated user.
    POST — Super Admin only.
    """

    queryset = (
        ULBDatabaseConfiguration.objects
        .select_related('ulb', 'application')
        .all()
        .order_by('ulb__ulb_name')
    )
    serializer_class = ULBDatabaseConfigurationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ULBDatabaseConfigDetailView(generics.RetrieveUpdateAPIView):
    """
    GET       — any authenticated user.
    PUT/PATCH — Super Admin only.
    """

    queryset = (
        ULBDatabaseConfiguration.objects
        .select_related('ulb', 'application')
        .all()
    )
    serializer_class = ULBDatabaseConfigurationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ULBApplicationListCreateView(generics.ListCreateAPIView):
    """
    GET  — any authenticated user.
    POST — Super Admin only.
    """

    queryset = (
        ULBApplication.objects
        .select_related('ulb', 'application')
        .all()
        .order_by('-start_date')
    )
    serializer_class = ULBApplicationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ULBApplicationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET       — any authenticated user.
    PUT/PATCH — Super Admin only.
    """

    queryset = (
        ULBApplication.objects
        .select_related('ulb', 'application')
        .all()
    )
    serializer_class = ULBApplicationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]
