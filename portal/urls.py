from django.urls import path
from . import views

urlpatterns = [
    # Dashboard — SUPER_ADMIN goes here; ULB_ADMIN is auto-routed to ulb-admin-dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # ── ULB Admin ─────────────────────────────────────────────────────────────
    path('ulb-admin/dashboard/', views.ULBAdminDashboardView.as_view(), name='ulb-admin-dashboard'),
    path('ulb-admin/create-user/', views.ULBAdminCreateUserView.as_view(), name='ulb-admin-create-user'),

    # ── End User ──────────────────────────────────────────────────────────────
    path('end-user/dashboard/', views.EndUserDashboardView.as_view(), name='end-user-dashboard'),

    # Applications
    path('applications/', views.ApplicationListView.as_view(), name='apps'),
    path('applications/add/', views.ApplicationAddView.as_view(), name='app-add'),
    path('applications/view/', views.ApplicationViewView.as_view(), name='app-view'),

    # ULBs
    path('ulbs/', views.ULBListView.as_view(), name='ulbs'),
    path('ulbs/add/', views.ULBAddView.as_view(), name='ulb-add'),
    path('ulbs/view/', views.ULBViewView.as_view(), name='ulb-view'),

    # ULB Database Configuration
    path('ulb-db-config/', views.ULBDatabaseConfigListView.as_view(), name='ulb-db-config'),
    path('ulb-db-config/add/', views.ULBDatabaseConfigAddView.as_view(), name='ulb-db-config-add'),
    path('ulb-db-config/view/', views.ULBDatabaseConfigViewView.as_view(), name='ulb-db-config-view'),

    # ULB Application
    path('ulb-app/', views.ULBApplicationListView.as_view(), name='ulb-app'),
    path('ulb-app/add/', views.ULBApplicationAddView.as_view(), name='ulb-app-add'),
    path('ulb-app/view/', views.ULBApplicationViewView.as_view(), name='ulb-app-view'),

    # Roles
    path('roles/', views.RoleListView.as_view(), name='role'),
    path('roles/add/', views.RoleAddView.as_view(), name='role-add'),
    path('roles/view/', views.RoleViewView.as_view(), name='role-view'),

    # Permissions
    path('permissions/', views.PermissionListView.as_view(), name='permission'),
    path('permissions/add/', views.PermissionAddView.as_view(), name='permission-add'),
    path('permissions/view/', views.PermissionViewView.as_view(), name='permission-view'),

    # Role-Permission
    path('role-permissions/', views.RolePermissionListView.as_view(), name='role-permission'),
    path('role-permissions/add/', views.RolePermissionAddView.as_view(), name='role-permission-add'),
    path('role-permissions/view/', views.RolePermissionViewView.as_view(), name='role-permission-view'),

    # User Application Access
    path('user-app-access/', views.UserAppAccessListView.as_view(), name='user-app-access'),
    path('user-app-access/add/', views.UserAppAccessAddView.as_view(), name='user-app-access-add'),
    path('user-app-access/view/', views.UserAppAccessViewView.as_view(), name='user-app-access-view'),

    # SSO Client
    path('sso-clients/', views.SSOClientListView.as_view(), name='sso-client'),
    path('sso-clients/add/', views.SSOClientAddView.as_view(), name='sso-client-add'),
    path('sso-clients/view/', views.SSOClientViewView.as_view(), name='sso-client-view'),

    # SSO Authorization
    path('sso-authorizations/', views.SSOAuthorizationListView.as_view(), name='sso-authorization'),
    path('sso-authorizations/add/', views.SSOAuthorizationAddView.as_view(), name='sso-authorization-add'),
    path('sso-authorizations/view/', views.SSOAuthorizationViewView.as_view(), name='sso-authorization-view'),

    # Change Password (portal-side, uses AppLauncher template)
    path('change-password/', views.ChangePasswordView.as_view(), name='portal-change-password'),
]
