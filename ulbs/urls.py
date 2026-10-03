from django.urls import path

from .views import (
    ULBListCreateView,
    ULBDetailView,
    ULBDatabaseConfigListCreateView,
    ULBDatabaseConfigDetailView,
    ULBApplicationListCreateView,
    ULBApplicationDetailView,
)

urlpatterns = [
    # ULB
    path('', ULBListCreateView.as_view(), name='ulb-list-create'),
    path('<int:pk>/', ULBDetailView.as_view(), name='ulb-detail'),

    # ULB Database Configuration
    path('db-configs/', ULBDatabaseConfigListCreateView.as_view(), name='ulb-db-config-list-create'),
    path('db-configs/<int:pk>/', ULBDatabaseConfigDetailView.as_view(), name='ulb-db-config-detail'),

    # ULB Application
    path('ulb-applications/', ULBApplicationListCreateView.as_view(), name='ulb-application-list-create'),
    path('ulb-applications/<int:pk>/', ULBApplicationDetailView.as_view(), name='ulb-application-detail'),
]
