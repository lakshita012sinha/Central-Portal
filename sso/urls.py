from django.urls import path
from . import views

urlpatterns = [
    # SSO authorize/token flow
    path('authorize/', views.authorize, name='sso-authorize'),
    path('token/',     views.token,     name='sso-token'),

    # SSO Client management
    path('clients/',            views.SSOClientListCreateView.as_view(), name='sso-client-list'),
    path('clients/<int:pk>/',   views.SSOClientDetailView.as_view(),     name='sso-client-detail'),

    # SSO Authorization Codes (read-only)
    path('auth-codes/',           views.SSOAuthorizationCodeListView.as_view(),   name='sso-auth-code-list'),
    path('auth-codes/<int:pk>/',  views.SSOAuthorizationCodeDetailView.as_view(), name='sso-auth-code-detail'),
]
