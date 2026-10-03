from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import BrowserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root redirect → dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Browser login (renders AppLauncher login template)
    path('login/', BrowserLoginView.as_view(), name='browser-login'),

    # Portal (all admin-panel browser views)
    path('', include('portal.urls')),

    # REST API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/ulbs/', include('ulbs.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/access-control/', include('access_control.urls')),

    # SSO flow
    path('sso/', include('sso.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
