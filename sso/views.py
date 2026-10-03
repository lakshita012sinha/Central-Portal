from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from access_control.models import (
    ULBApplicationAccess,
    UserApplicationAccess,
)
from .models import SSOAuthorizationCode, SSOClient


@login_required
def authorize(request):

    client_id = request.GET.get('client_id')
    redirect_uri = request.GET.get('redirect_uri')

    if not client_id:
        return JsonResponse(
            {
                'error': 'client_id is required'
            },
            status=400
        )

    if not redirect_uri:
        return JsonResponse(
            {
                'error': 'redirect_uri is required'
            },
            status=400
        )

    #  Validate SSO Client
    

    try:
        client = SSOClient.objects.select_related(
            'application'
        ).get(
            client_id=client_id,
            is_active=True
        )
    except SSOClient.DoesNotExist:
        return JsonResponse(
            {
                'error': 'Invalid or inactive client'
            },
            status=400
        )

    
    # Validate Redirect URI

    if redirect_uri != client.allowed_redirect_uri:
        return JsonResponse(
            {
                'error': 'Invalid redirect_uri'
            },
            status=400
        )
    if client.application.status != 'ACTIVE':
        return JsonResponse(
             {
                'error': 'Application is not active'
             },
             status=403
       )
    
    # Get User's ULB Membership


    membership = (
        request.user.ulb_memberships
        .select_related('ulb')
        .filter(is_active=True)
        .first()
    )

    if not membership:
        return JsonResponse(
            {
                'error': 'User does not have an active ULB membership'
            },
            status=403
        )

    ulb = membership.ulb

    # Validate ULB

    today = timezone.localdate()

    if not ulb.is_active:
        return JsonResponse(
            {
                'error': 'ULB is inactive'
            },
            status=403
        )

    if ulb.status != 'ACTIVE':
        return JsonResponse(
            {
                'error': 'ULB is not active'
            },
            status=403
        )

    if ulb.valid_from > today:
        return JsonResponse(
            {
                'error': 'ULB validity has not started'
            },
            status=403
        )

    if ulb.valid_to and ulb.valid_to < today:
        return JsonResponse(
            {
                'error': 'ULB tenure has expired'
            },
            status=403
        )

    #Validate ULB → Application Grant

    ulb_application = (
        ULBApplicationAccess.objects
        .filter(
            ulb=ulb,
            application=client.application,
            is_active=True
        )
        .first()
    )

    if not ulb_application:
        return JsonResponse(
            {
                'error': 'Application is not granted to this ULB'
            },
            status=403
        )

    if ulb_application.start_date > today:
        return JsonResponse(
            {
                'error': 'Application access has not started'
            },
            status=403
        )

    if (
        ulb_application.end_date
        and ulb_application.end_date < today
    ):
        return JsonResponse(
            {
                'error': 'Application access has expired'
            },
            status=403
        )

    # Validate User → Application Access

    user_access = (
        UserApplicationAccess.objects
        .select_related('role')
        .filter(
            user=request.user,
            ulb=ulb,
            application=client.application,
            is_active=True
        )
        .first()
    )

    if not user_access:
        return JsonResponse(
            {
                'error': 'User does not have access to this application'
            },
            status=403
        )

    if user_access.start_date > today:
        return JsonResponse(
            {
                'error': 'User application access has not started'
            },
            status=403
        )

    if (
        user_access.end_date
        and user_access.end_date < today
    ):
        return JsonResponse(
            {
                'error': 'User application access has expired'
            },
            status=403
        )

    # Generate Authorization Code

    expires_at = timezone.now() + timedelta(
        seconds=client.code_expiry_seconds
    )

    authorization_code = SSOAuthorizationCode.objects.create(
        client=client,
        user=request.user,
        ulb=ulb,
        redirect_uri=redirect_uri,
        expires_at=expires_at,
    )

    # Redirect to Application

    separator = '&' if '?' in redirect_uri else '?'

    redirect_url = (
        f"{redirect_uri}"
        f"{separator}"
        f"code={authorization_code.code}"
    )

    return redirect(redirect_url)

@csrf_exempt
def token(request):
    if request.method != 'POST':
        return JsonResponse(
            {
                'error': 'method_not_allowed',
                'error_description': 'Only POST requests are allowed.'
            },
            status=405
        )

    client_id = request.POST.get('client_id')
    client_secret = request.POST.get('client_secret')
    code = request.POST.get('code')
    redirect_uri = request.POST.get('redirect_uri')

    # Validate required parameters

    if not client_id:
        return JsonResponse(
            {
                'error': 'invalid_request',
                'error_description': 'client_id is required.'
            },
            status=400
        )

    if not client_secret:
        return JsonResponse(
            {
                'error': 'invalid_request',
                'error_description': 'client_secret is required.'
            },
            status=400
        )

    if not code:
        return JsonResponse(
            {
                'error': 'invalid_request',
                'error_description': 'code is required.'
            },
            status=400
        )

    if not redirect_uri:
        return JsonResponse(
            {
                'error': 'invalid_request',
                'error_description': 'redirect_uri is required.'
            },
            status=400
        )

    # Validate SSO Client

    try:
        client = SSOClient.objects.select_related(
            'application'
        ).get(
            client_id=client_id,
            is_active=True
        )
    except SSOClient.DoesNotExist:
        return JsonResponse(
            {
                'error': 'invalid_client',
                'error_description': 'Invalid or inactive client.'
            },
            status=401
        )

    # Validate Client Secret

    if client.client_secret != client_secret:
        return JsonResponse(
            {
                'error': 'invalid_client',
                'error_description': 'Invalid client credentials.'
            },
            status=401
        )

    # Validate Redirect URI

    if redirect_uri != client.allowed_redirect_uri:
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Invalid redirect_uri.'
            },
            status=400
        )

    # Validate Application

    if client.application.status != 'ACTIVE':
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Application is not active.'
            },
            status=403
        )

    # Validate Authorization Code

    try:
        authorization_code = SSOAuthorizationCode.objects.select_related(
            'client',
            'user',
            'ulb',
        ).get(
            code=code
        )
    except (SSOAuthorizationCode.DoesNotExist, ValueError):
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Invalid authorization code.'
            },
            status=400
        )

    # Validate that code belongs to this client

    if authorization_code.client_id != client.id:
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Authorization code was not issued to this client.'
            },
            status=400
        )

    # Validate redirect URI stored with authorization code

    if authorization_code.redirect_uri != redirect_uri:
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Redirect URI does not match the authorization code.'
            },
            status=400
        )

    # Validate authorization code is not already used

    if authorization_code.used_at is not None:
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Authorization code has already been used.'
            },
            status=400
        )

    # Validate authorization code expiry

    if timezone.now() >= authorization_code.expires_at:
        return JsonResponse(
            {
                'error': 'invalid_grant',
                'error_description': 'Authorization code has expired.'
            },
            status=400
        )

    # Validate User

    if not authorization_code.user.is_active:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'User account is inactive.'
            },
            status=403
        )

    # Validate ULB

    ulb = authorization_code.ulb
    today = timezone.localdate()

    if not ulb.is_active:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'ULB is inactive.'
            },
            status=403
        )

    if ulb.status != 'ACTIVE':
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'ULB is not active.'
            },
            status=403
        )

    if ulb.valid_from > today:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'ULB validity has not started.'
            },
            status=403
        )

    if ulb.valid_to and ulb.valid_to < today:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'ULB tenure has expired.'
            },
            status=403
        )

    # Validate ULB → Application Access

    ulb_application = (
        ULBApplicationAccess.objects
        .filter(
            ulb=ulb,
            application=client.application,
            is_active=True,
            start_date__lte=today,
        )
        .filter(
            models.Q(end_date__isnull=True) |
            models.Q(end_date__gte=today)
        )
        .first()
    )

    if not ulb_application:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'Application access is not valid for this ULB.'
            },
            status=403
        )

    # Validate User → Application Access

    user_access = (
        UserApplicationAccess.objects
        .select_related('role')
        .filter(
            user=authorization_code.user,
            ulb=ulb,
            application=client.application,
            is_active=True,
            start_date__lte=today,
        )
        .filter(
            models.Q(end_date__isnull=True) |
            models.Q(end_date__gte=today)
        )
        .first()
    )

    if not user_access:
        return JsonResponse(
            {
                'error': 'access_denied',
                'error_description': 'User does not have valid application access.'
            },
            status=403
        )

    # Atomically mark authorization code as USED

    with transaction.atomic():
        authorization_code = (
            SSOAuthorizationCode.objects
            .select_for_update()
            .select_related(
                'user',
                'ulb',
                'client__application',
            )
            .get(
                id=authorization_code.id
            )
        )

        if authorization_code.used_at is not None:
            return JsonResponse(
                {
                    'error': 'invalid_grant',
                    'error_description': 'Authorization code has already been used.'
                },
                status=400
            )

        if timezone.now() >= authorization_code.expires_at:
            return JsonResponse(
                {
                    'error': 'invalid_grant',
                    'error_description': 'Authorization code has expired.'
                },
                status=400
            )

        authorization_code.used_at = timezone.now()
        authorization_code.save(
            update_fields=['used_at']
        )

    # Return trusted identity information

    return JsonResponse(
        {
            'access_token': None,
            'token_type': 'Bearer',
            'user': {
                'id': authorization_code.user.id,
                'username': authorization_code.user.username,
                'first_name': authorization_code.user.first_name,
                'last_name': authorization_code.user.last_name,
                'email': authorization_code.user.email,
                'mobile': authorization_code.user.mobile,
            },
            'ulb': {
                'id': ulb.id,
                'code': ulb.ulb_code,
                'name': ulb.ulb_name,
            },
            'application': {
                'id': client.application.id,
                'code': client.application.application_code,
                'name': client.application.application_name,
            },
            'role': {
                'id': user_access.role.id if user_access.role else None,
                'name': user_access.role.role_name if user_access.role else None,
                'code': user_access.role.role_code if user_access.role else None,
            }
        },
        status=200
    )


# ── SSO Client CRUD ────────────────────────────────────────────────────────────

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from access_control.permissions import IsSuperAdmin
from .serializers import SSOClientSerializer, SSOAuthorizationCodeSerializer


class SSOClientListCreateView(generics.ListCreateAPIView):
    """GET — any authenticated user. POST — Super Admin only."""

    queryset = (
        SSOClient.objects
        .select_related('application')
        .all()
        .order_by('application__application_name')
    )
    serializer_class = SSOClientSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class SSOClientDetailView(generics.RetrieveUpdateAPIView):
    """GET — any authenticated user. PUT/PATCH — Super Admin only."""

    queryset = SSOClient.objects.select_related('application').all()
    serializer_class = SSOClientSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]


class SSOAuthorizationCodeListView(generics.ListAPIView):
    """Read-only list of all SSO authorization codes. Super Admin only."""

    queryset = (
        SSOAuthorizationCode.objects
        .select_related('client__application', 'user', 'ulb')
        .all()
        .order_by('-created_at')
    )
    serializer_class = SSOAuthorizationCodeSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]


class SSOAuthorizationCodeDetailView(generics.RetrieveAPIView):
    """Read-only detail of a single SSO authorization code. Super Admin only."""

    queryset = (
        SSOAuthorizationCode.objects
        .select_related('client__application', 'user', 'ulb')
        .all()
    )
    serializer_class = SSOAuthorizationCodeSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
