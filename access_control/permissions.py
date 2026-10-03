from rest_framework.permissions import BasePermission
from ulbs.models import ULBMembership


class IsSuperAdmin(BasePermission):

    message = 'Super Admin access required.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsULBAdmin(BasePermission):
    """Grants access only to users with ULB_ADMIN membership."""

    message = 'ULB Admin access required.'

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return ULBMembership.objects.filter(
            user=request.user,
            user_type='ULB_ADMIN',
            is_active=True,
            ulb__is_active=True,
        ).exists()


def get_ulb_admin_membership(user):
    """
    Returns the active ULB_ADMIN membership for a user, or None.
    Helper used by views to retrieve the ULB the admin belongs to.
    """
    return (
        ULBMembership.objects
        .select_related('ulb')
        .filter(
            user=user,
            user_type='ULB_ADMIN',
            is_active=True,
            ulb__is_active=True,
        )
        .first()
    )
