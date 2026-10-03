from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import (
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ULBUserCreateSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        return Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )


class BrowserLoginView(View):

    def get(self, request):
        # Already logged in → go to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')

        next_url = request.GET.get('next', '/dashboard/')

        return render(
            request,
            'login.html',
            {
                'next': next_url,
            }
        )

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/dashboard/')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:
            return render(
                request,
                'login.html',
                {
                    'error': 'Invalid username or password.',
                    'next': next_url,
                    'username': username,
                },
                status=400
            )

        if not user.is_active:
            return render(
                request,
                'login.html',
                {
                    'error': 'Your account is inactive.',
                    'next': next_url,
                    'username': username,
                },
                status=403
            )

        login(request, user)

        return redirect(next_url)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {
                'message': 'Logout successful.'
            },
            status=status.HTTP_200_OK
        )


class BrowserLogoutView(View):
    """POST → logout session → redirect to login page."""

    def post(self, request):
        logout(request)
        return redirect('browser-login')


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )

class ULBUserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not request.user.is_superuser:
            return Response(
                {
                    'detail': 'Only Super Admin can create ULB users.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ULBUserCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                'message': 'ULB user created successfully.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        user = request.user

        user.set_password(
            serializer.validated_data['new_password']
        )

        user.force_password_change = False

        user.save(
            update_fields=[
                'password',
                'force_password_change'
            ]
        )

        # Important:
        # set_password() changes the password hash,
        # so Django's session must be refreshed.
        login(request, user)

        return Response(
            {
                'message': 'Password changed successfully.'
            },
            status=status.HTTP_200_OK
        )    

class BrowserChangePasswordView(View):

    def get(self, request):
        if not request.user.is_authenticated:
           return redirect('/login/?next=/change-password/')
        return render(
            request,
            'change-password.html'
        )

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/?next=/change-password/')

        serializer = ChangePasswordSerializer(
            data={
                'old_password': request.POST.get('old_password'),
                'new_password': request.POST.get('new_password'),
                'confirm_password': request.POST.get('confirm_password'),
            },
            context={'request': request}
        )

        if not serializer.is_valid():
            error_messages = []

            for field_errors in serializer.errors.values():
                error_messages.extend(
                    [str(error) for error in field_errors]
                )

            return render(
                request,
                'change-password.html',
                {
                    'error': ' '.join(error_messages),
                },
                status=400
            )

        user = request.user

        user.set_password(
            serializer.validated_data['new_password']
        )

        user.force_password_change = False

        user.save(
            update_fields=[
                'password',
                'force_password_change'
            ]
        )

        login(request, user)

        return render(
            request,
            'change-password.html',
            {
                'success': 'Password changed successfully.'
            }
        )    


class UserListView(APIView):
    """List all users for dropdown population (authenticated users only)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import User
        users = User.objects.filter(
            is_active=True
        ).order_by('username').values(
            'id', 'username', 'first_name', 'last_name', 'email'
        )
        return Response(list(users), status=status.HTTP_200_OK)


# ── ULB Admin: create end-user ────────────────────────────────────────────────

class ULBAdminUserCreateView(APIView):
    """
    POST /api/accounts/ulb-admin/users/
    Allows a ULB_ADMIN to create an END_USER within their own ULB.
    Enforces: same ULB, only granted apps, no cross-ULB creation.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from access_control.permissions import IsULBAdmin, get_ulb_admin_membership
        from .serializers import ULBAdminUserCreateSerializer

        # Must be ULB_ADMIN
        perm_check = IsULBAdmin()
        if not perm_check.has_permission(request, self):
            return Response(
                {'detail': 'ULB Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ULBAdminUserCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'message': 'User created successfully.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )


class ULBAdminMyUsersView(APIView):
    """
    GET /api/accounts/ulb-admin/users/
    Returns all END_USERs in the ULB_ADMIN's ULB.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from access_control.permissions import IsULBAdmin, get_ulb_admin_membership

        perm_check = IsULBAdmin()
        if not perm_check.has_permission(request, self):
            return Response(
                {'detail': 'ULB Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        membership = get_ulb_admin_membership(request.user)
        if not membership:
            return Response([], status=status.HTTP_200_OK)

        from ulbs.models import ULBMembership
        user_ids = (
            ULBMembership.objects
            .filter(ulb=membership.ulb, is_active=True)
            .exclude(user=request.user)
            .values_list('user_id', flat=True)
        )

        from .models import User
        users = User.objects.filter(id__in=user_ids, is_active=True).order_by('username')
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)


class ULBAdminULBAppsView(APIView):
    """
    GET /api/accounts/ulb-admin/apps/
    Returns all active applications assigned to the ULB_ADMIN's ULB.
    Checks both ULBApplication and ULBApplicationAccess tables.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from access_control.permissions import IsULBAdmin, get_ulb_admin_membership

        perm_check = IsULBAdmin()
        if not perm_check.has_permission(request, self):
            return Response(
                {'detail': 'ULB Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        membership = get_ulb_admin_membership(request.user)
        if not membership:
            return Response([], status=status.HTTP_200_OK)

        ulb = membership.ulb

        from django.utils import timezone
        from django.db.models import Q
        from ulbs.models import ULBApplication
        from access_control.models import ULBApplicationAccess
        from applications.models import Application

        today = timezone.localdate()

        # IDs from ULBApplication (primary grant table)
        ids_from_ulb_app = set(
            ULBApplication.objects
            .filter(ulb=ulb, status='ACTIVE')
            .values_list('application_id', flat=True)
        )

        # IDs from ULBApplicationAccess (secondary grant table)
        ids_from_access = set(
            ULBApplicationAccess.objects
            .filter(ulb=ulb, is_active=True, start_date__lte=today)
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=today))
            .values_list('application_id', flat=True)
        )

        all_granted_ids = ids_from_ulb_app | ids_from_access

        apps = (
            Application.objects
            .filter(id__in=all_granted_ids, status='ACTIVE')
            .order_by('display_order', 'application_name')
        )

        from applications.serializers import ApplicationSerializer
        return Response(
            ApplicationSerializer(apps, many=True).data,
            status=status.HTTP_200_OK
        )


# ── END USER: my apps with SSO launch info ────────────────────────────────────

class EndUserMyAppsView(APIView):
    """
    GET /api/accounts/end-user/my-apps/
    Returns the current user's permitted applications with SSO launch details.
    Only returns apps the user genuinely has active UserApplicationAccess for.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        from django.db.models import Q
        from access_control.models import UserApplicationAccess
        from sso.models import SSOClient

        today = timezone.localdate()

        # All active, in-date UserApplicationAccess records for this user
        accesses = (
            UserApplicationAccess.objects
            .filter(
                user=request.user,
                is_active=True,
                ulb__is_active=True,
                application__status='ACTIVE',
                start_date__lte=today,
            )
            .filter(
                Q(end_date__isnull=True) | Q(end_date__gte=today)
            )
            .select_related('application', 'ulb', 'role')
            .order_by('application__display_order', 'application__application_name')
        )

        # Build a map of application_id → SSO client info
        app_ids = [a.application_id for a in accesses]
        sso_clients = {
            sc.application_id: sc
            for sc in SSOClient.objects.filter(
                application_id__in=app_ids,
                is_active=True,
            ).select_related('application')
        }

        result = []
        for access in accesses:
            app = access.application
            sso = sso_clients.get(app.id)

            result.append({
                'application_id':   app.id,
                'application_code': app.application_code,
                'application_name': app.application_name,
                'icon':             app.icon or None,
                'launch_url':       app.launch_url,
                'ulb_id':           access.ulb.id,
                'ulb_name':         access.ulb.ulb_name,
                # SSO fields — None if no SSO client configured for this app
                'sso_client_id':      sso.client_id          if sso else None,
                'sso_redirect_uri':   sso.allowed_redirect_uri if sso else None,
                'has_sso':            sso is not None,
            })

        return Response(result, status=status.HTTP_200_OK)
