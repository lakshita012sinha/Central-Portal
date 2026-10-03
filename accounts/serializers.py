from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from django.db.models import Q
from .models import User
from ulbs.models import ULBMembership, ULB
from access_control.models import UserApplicationAccess


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        attrs['user'] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):

    memberships = serializers.SerializerMethodField()

    application_access = serializers.SerializerMethodField()

    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'is_active',
            'is_staff',
            'is_superuser',
            'force_password_change',
            'user_type',
            'memberships',
            'application_access',
        ]

        read_only_fields = [
            'id',
            'is_staff',
            'is_superuser',
            'user_type',
            'memberships',
            'application_access',
        ]

    def get_memberships(self, obj):
        memberships = (
            ULBMembership.objects
            .filter(
                user=obj,
                is_active=True,
                ulb__is_active=True
            )
            .select_related('ulb')
        )

        return ULBMembershipSerializer(
            memberships,
            many=True
        ).data

    def get_application_access(self, obj):
        today = timezone.localdate()

        accesses = (
            UserApplicationAccess.objects
            .filter(
                user=obj,
                is_active=True,
                ulb__is_active=True,
                application__status='ACTIVE',
            )
            .filter(
                start_date__lte=today
            )
            .filter(
                Q(
                    end_date__isnull=True
                ) |
                Q(
                    end_date__gte=today
                )
            )
            .select_related(
                'ulb',
                'application',
                'role'
            )
        )

        return UserApplicationAccessSerializer(
            accesses,
            many=True
        ).data

    def get_user_type(self, obj):

        if obj.is_superuser:
            return 'SUPER_ADMIN'

        membership = (
            ULBMembership.objects
            .filter(
                user=obj,
                is_active=True,
                ulb__is_active=True
            )
            .first()
        )

        if membership:
            return membership.user_type

        return None

class ULBMembershipSerializer(serializers.ModelSerializer):

    ulb_id = serializers.IntegerField(
        source='ulb.id',
        read_only=True
    )

    ulb_code = serializers.CharField(
        source='ulb.ulb_code',
        read_only=True
    )

    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    ulb_status = serializers.CharField(
        source='ulb.status',
        read_only=True
    )

    class Meta:
        model = ULBMembership
        fields = [
            'ulb_id',
            'ulb_code',
            'ulb_name',
            'ulb_status',
            'user_type',
            'is_active',
            'created_at',
        ]

class UserApplicationAccessSerializer(serializers.ModelSerializer):

    application_id = serializers.IntegerField(
        source='application.id',
        read_only=True
    )

    application_code = serializers.CharField(
        source='application.application_code',
        read_only=True
    )

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    application_status = serializers.CharField(
        source='application.status',
        read_only=True
    )

    ulb_id = serializers.IntegerField(
        source='ulb.id',
        read_only=True
    )

    ulb_code = serializers.CharField(
        source='ulb.ulb_code',
        read_only=True
    )

    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    role_id = serializers.IntegerField(
        source='role.id',
        read_only=True,
        allow_null=True
    )

    role_name = serializers.CharField(
        source='role.role_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = UserApplicationAccess
        fields = [
            'application_id',
            'application_code',
            'application_name',
            'application_status',
            'ulb_id',
            'ulb_code',
            'ulb_name',
            'role_id',
            'role_name',
            'start_date',
            'end_date',
            'is_active',
        ]        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        user = self.context['request'].user

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check old password
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                'old_password': 'Old password is incorrect.'
            })

        # Check new password confirmation
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        # Prevent same password
        if old_password == new_password:
            raise serializers.ValidationError({
                'new_password': 'New password must be different from old password.'
            })

        # Use Django's password validators
        from django.contrib.auth.password_validation import validate_password

        validate_password(
            new_password,
            user
        )

        return attrs        

class ULBUserCreateSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True
    )

    mobile = serializers.CharField(
        max_length=15,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    ulb = serializers.PrimaryKeyRelatedField(
        queryset=ULB.objects.all()
    )

    user_type = serializers.ChoiceField(
        choices=ULBMembership.USER_TYPE_CHOICES
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'A user with this username already exists.'
            )

        return value

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        ulb = attrs['ulb']

        if not ulb.is_active:
            raise serializers.ValidationError({
                'ulb': 'Cannot create a user for an inactive ULB.'
            })

        if ulb.status != 'ACTIVE':
            raise serializers.ValidationError({
                'ulb': 'Cannot create a user for an inactive or suspended ULB.'
            })

        validate_password(
            attrs['password']
        )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        validated_data.pop('confirm_password')

        ulb = validated_data.pop('ulb')
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            is_active=True,
            force_password_change=True,
            **validated_data
        )

        ULBMembership.objects.create(
            user=user,
            ulb=ulb,
            user_type=user_type,
            is_active=True
        )

        return user    


class ULBAdminUserCreateSerializer(serializers.Serializer):
    """
    Used by ULB_ADMIN to create an END_USER within their own ULB.

    Enforces:
    - The new user is always created as END_USER in the admin's ULB.
    - application_ids must be a subset of apps granted to that ULB.
    - start_date defaults to today if omitted.
    - All records created atomically: User + ULBMembership + UserApplicationAccess (one per app).
    """

    username = serializers.CharField(max_length=150)

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    application_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text='IDs of applications to grant access to (must belong to the admin\'s ULB).'
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'A user with this username already exists.'
            )
        return value

    def validate(self, attrs):
        # Password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        validate_password(attrs['password'])

        # Resolve which ULB this admin belongs to
        request = self.context['request']

        from access_control.permissions import get_ulb_admin_membership
        membership = get_ulb_admin_membership(request.user)

        if not membership:
            raise serializers.ValidationError(
                'You do not have an active ULB_ADMIN membership.'
            )

        ulb = membership.ulb

        if ulb.status != 'ACTIVE':
            raise serializers.ValidationError(
                'Your ULB is not active.'
            )

        # Validate requested application_ids are all granted to this ULB.
        # Check both ULBApplication (primary) AND ULBApplicationAccess (secondary).
        from ulbs.models import ULBApplication
        from access_control.models import ULBApplicationAccess
        from applications.models import Application

        requested_ids = set(attrs['application_ids'])

        # Gather app IDs from ULBApplication (ulb_grants)
        granted_via_ulb_app = set(
            ULBApplication.objects
            .filter(ulb=ulb, status='ACTIVE')
            .values_list('application_id', flat=True)
        )

        # Gather app IDs from ULBApplicationAccess (ulb_access)
        from django.utils import timezone
        today = timezone.localdate()
        granted_via_access = set(
            ULBApplicationAccess.objects
            .filter(
                ulb=ulb,
                is_active=True,
                start_date__lte=today,
            )
            .filter(
                Q(end_date__isnull=True) | Q(end_date__gte=today)
            )
            .values_list('application_id', flat=True)
        )

        all_granted = granted_via_ulb_app | granted_via_access

        not_allowed = requested_ids - all_granted
        if not_allowed:
            raise serializers.ValidationError({
                'application_ids': (
                    f'Application(s) {sorted(not_allowed)} are not granted to your ULB.'
                )
            })

        # Verify all IDs actually exist as Application objects
        found_apps = list(
            Application.objects
            .filter(id__in=requested_ids, status='ACTIVE')
        )

        if len(found_apps) != len(requested_ids):
            found_ids = {a.id for a in found_apps}
            missing = requested_ids - found_ids
            raise serializers.ValidationError({
                'application_ids': f'Application(s) {sorted(missing)} not found or inactive.'
            })

        attrs['_ulb'] = ulb
        attrs['_applications'] = found_apps
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        ulb         = validated_data['_ulb']
        applications = validated_data['_applications']
        password    = validated_data['password']

        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            is_active=True,
            force_password_change=True,
        )

        ULBMembership.objects.create(
            user=user,
            ulb=ulb,
            user_type='END_USER',
            is_active=True,
        )

        from django.utils import timezone
        today = timezone.localdate()

        from access_control.models import UserApplicationAccess
        for app in applications:
            UserApplicationAccess.objects.create(
                user=user,
                ulb=ulb,
                application=app,
                role=None,
                start_date=today,
                end_date=None,
                is_active=True,
            )

        return user
