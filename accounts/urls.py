from django.urls import path
from .views import (
    LoginView,
    BrowserLoginView,
    BrowserChangePasswordView,
    BrowserLogoutView,
    LogoutView,
    CurrentUserView,
    ChangePasswordView,
    ULBUserCreateView,
    UserListView,
    ULBAdminUserCreateView,
    ULBAdminMyUsersView,
    ULBAdminULBAppsView,
    EndUserMyAppsView,
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('browser-login/', BrowserLoginView.as_view(), name='browser-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('browser-logout/', BrowserLogoutView.as_view(), name='browser-logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('browser-change-password/', BrowserChangePasswordView.as_view(), name='browser-change-password'),

    # Super Admin: create ULB user
    path('users/', ULBUserCreateView.as_view(), name='create-ulb-user'),
    path('users/list/', UserListView.as_view(), name='user-list'),

    # ULB Admin endpoints
    path('ulb-admin/users/', ULBAdminUserCreateView.as_view(), name='ulb-admin-user-create'),
    path('ulb-admin/my-users/', ULBAdminMyUsersView.as_view(), name='ulb-admin-my-users'),
    path('ulb-admin/apps/', ULBAdminULBAppsView.as_view(), name='ulb-admin-apps'),

    # End User endpoints
    path('end-user/my-apps/', EndUserMyAppsView.as_view(), name='end-user-my-apps'),
]