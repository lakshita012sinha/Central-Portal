from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class ForcePasswordChangeMixin:
    """Redirect to change-password if user must change their password."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(
            request.user, 'force_password_change', False
        ):
            if request.path != '/change-password/':
                return redirect('portal-change-password')
        return super().dispatch(request, *args, **kwargs)


class PortalView(ForcePasswordChangeMixin, LoginRequiredMixin, TemplateView):
    """Base class for all portal views — requires login."""
    pass


# ── Dashboard ────────────────────────────────────────────────────────────────

class DashboardView(PortalView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            from access_control.permissions import get_ulb_admin_membership
            from ulbs.models import ULBMembership
            if get_ulb_admin_membership(request.user):
                return redirect('ulb-admin-dashboard')
            # Route END_USER to their app launcher
            is_end_user = ULBMembership.objects.filter(
                user=request.user,
                user_type='END_USER',
                is_active=True,
                ulb__is_active=True,
            ).exists()
            if is_end_user:
                return redirect('end-user-dashboard')
        return super().dispatch(request, *args, **kwargs)


# ── Applications ─────────────────────────────────────────────────────────────

class ApplicationListView(PortalView):
    template_name = 'apps.html'


class ApplicationAddView(PortalView):
    template_name = 'app-add.html'


class ApplicationViewView(PortalView):
    template_name = 'app-view.html'


# ── ULBs ─────────────────────────────────────────────────────────────────────

class ULBListView(PortalView):
    template_name = 'ulbs.html'


class ULBAddView(PortalView):
    template_name = 'ulb-add.html'


class ULBViewView(PortalView):
    template_name = 'ulb-view.html'


# ── ULB Database Configuration ───────────────────────────────────────────────

class ULBDatabaseConfigListView(PortalView):
    template_name = 'ulb-db-config.html'


class ULBDatabaseConfigAddView(PortalView):
    template_name = 'ulb-db-config-add.html'


class ULBDatabaseConfigViewView(PortalView):
    template_name = 'ulb-db-config-view.html'


# ── ULB Application ───────────────────────────────────────────────────────────

class ULBApplicationListView(PortalView):
    template_name = 'ulb-app.html'


class ULBApplicationAddView(PortalView):
    template_name = 'ulb-app-add.html'


class ULBApplicationViewView(PortalView):
    template_name = 'ulb-app-view.html'


# ── Roles ─────────────────────────────────────────────────────────────────────

class RoleListView(PortalView):
    template_name = 'role.html'


class RoleAddView(PortalView):
    template_name = 'role-add.html'


class RoleViewView(PortalView):
    template_name = 'role-view.html'


# ── Permissions ───────────────────────────────────────────────────────────────

class PermissionListView(PortalView):
    template_name = 'permission.html'


class PermissionAddView(PortalView):
    template_name = 'permission-add.html'


class PermissionViewView(PortalView):
    template_name = 'permission-view.html'


# ── Role-Permission ───────────────────────────────────────────────────────────

class RolePermissionListView(PortalView):
    template_name = 'role-permission.html'


class RolePermissionAddView(PortalView):
    template_name = 'role-permission-add.html'


class RolePermissionViewView(PortalView):
    template_name = 'role-permission-view.html'


# ── User Application Access ───────────────────────────────────────────────────

class UserAppAccessListView(PortalView):
    template_name = 'user-app-access.html'


class UserAppAccessAddView(PortalView):
    template_name = 'user-app-access-add.html'


class UserAppAccessViewView(PortalView):
    template_name = 'user-app-access-view.html'


# ── SSO Client ────────────────────────────────────────────────────────────────

class SSOClientListView(PortalView):
    template_name = 'sso-client.html'


class SSOClientAddView(PortalView):
    template_name = 'sso-client-add.html'


class SSOClientViewView(PortalView):
    template_name = 'sso-client-view.html'


# ── SSO Authorization ─────────────────────────────────────────────────────────

class SSOAuthorizationListView(PortalView):
    template_name = 'sso-authorization.html'


class SSOAuthorizationAddView(PortalView):
    template_name = 'sso-authorization-add.html'


class SSOAuthorizationViewView(PortalView):
    template_name = 'sso-authorization-view.html'


# ── Change Password ───────────────────────────────────────────────────────────

class ChangePasswordView(PortalView):
    template_name = 'change-password.html'


# ── ULB Admin views ───────────────────────────────────────────────────────────

class ULBAdminMixin:
    """Restrict portal pages to ULB_ADMIN users only."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from access_control.permissions import get_ulb_admin_membership
            if not get_ulb_admin_membership(request.user):
                # Not a ULB_ADMIN — redirect to main dashboard
                return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class ULBAdminDashboardView(ULBAdminMixin, PortalView):
    """Dashboard for ULB_ADMIN: shows only their ULB's assigned applications."""
    template_name = 'ulb-admin-dashboard.html'


class ULBAdminCreateUserView(ULBAdminMixin, PortalView):
    """Create END_USER form for ULB_ADMIN."""
    template_name = 'ulb-admin-create-user.html'


# ── End User dashboard ────────────────────────────────────────────────────────

class EndUserMixin:
    """Restrict to END_USER only; redirect others to their correct dashboard."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('dashboard')
            from access_control.permissions import get_ulb_admin_membership
            if get_ulb_admin_membership(request.user):
                return redirect('ulb-admin-dashboard')
        return super().dispatch(request, *args, **kwargs)


class EndUserDashboardView(EndUserMixin, PortalView):
    """App launcher for END_USER: shows only their assigned applications."""
    template_name = 'end-user-dashboard.html'
