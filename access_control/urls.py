from rest_framework.routers import DefaultRouter

from .views import (
    ULBApplicationAccessViewSet,
    RoleViewSet,
    PermissionViewSet,
    RolePermissionViewSet,
    UserApplicationAccessViewSet,
)


router = DefaultRouter()

router.register(
    r'ulb-applications',
    ULBApplicationAccessViewSet,
    basename='ulb-application-access'
)

router.register(
    r'roles',
    RoleViewSet,
    basename='role'
)

router.register(
    r'permissions',
    PermissionViewSet,
    basename='permission'
)

router.register(
    r'role-permissions',
    RolePermissionViewSet,
    basename='role-permission'
)

router.register(
    r'user-application-access',
    UserApplicationAccessViewSet,
    basename='user-application-access'
) 

urlpatterns = router.urls

