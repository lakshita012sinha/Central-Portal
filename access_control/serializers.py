from rest_framework import serializers

from .models import (
    ULBApplicationAccess,
    Role,
    Permission,
    RolePermission,
    UserApplicationAccess
)

class ULBApplicationAccessSerializer(serializers.ModelSerializer):

    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    ulb_code = serializers.CharField(
        source='ulb.ulb_code',
        read_only=True
    )

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    application_code = serializers.CharField(
        source='application.application_code',
        read_only=True
    )

    class Meta:
        model = ULBApplicationAccess

        fields = [
            'id',
            'ulb',
            'ulb_code',
            'ulb_name',
            'application',
            'application_code',
            'application_name',
            'start_date',
            'end_date',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'ulb_code',
            'ulb_name',
            'application_code',
            'application_name',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'End date cannot be earlier than start date.'
            })

        return attrs

class RoleSerializer(serializers.ModelSerializer):

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    class Meta:
        model = Role

        fields = [
            'id',
            'role_name',
            'role_code',
            'description',
            'role_type',
            'application',
            'application_name',
            'ulb',
            'ulb_name',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'application_name',
            'ulb_name',
            'created_at',
            'updated_at',
        ]       

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission

        fields = [
            'id',
            'permission_name',
            'permission_code',
            'description',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]         

class RolePermissionSerializer(serializers.ModelSerializer):

    role_name = serializers.CharField(
        source='role.role_name',
        read_only=True
    )

    role_code = serializers.CharField(
        source='role.role_code',
        read_only=True
    )

    permission_name = serializers.CharField(
        source='permission.permission_name',
        read_only=True
    )

    permission_code = serializers.CharField(
        source='permission.permission_code',
        read_only=True
    )

    class Meta:
        model = RolePermission

        fields = [
            'id',
            'role',
            'role_name',
            'role_code',
            'permission',
            'permission_name',
            'permission_code',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'role_name',
            'role_code',
            'permission_name',
            'permission_code',
            'created_at',
        ]        

class UserApplicationAccessSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    ulb_name = serializers.CharField(source='ulb.ulb_name', read_only=True)
    ulb_code = serializers.CharField(source='ulb.ulb_code', read_only=True)

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )
    application_code = serializers.CharField(
        source='application.application_code',
        read_only=True
    )

    role_name = serializers.CharField(
        source='role.role_name',
        read_only=True
    )
    role_code = serializers.CharField(
        source='role.role_code',
        read_only=True
    )

    class Meta:
        model = UserApplicationAccess
        fields = [
            'id',
            'user',
            'username',
            'user_email',
            'ulb',
            'ulb_code',
            'ulb_name',
            'application',
            'application_code',
            'application_name',
            'role',
            'role_code',
            'role_name',
            'start_date',
            'end_date',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'username',
            'user_email',
            'ulb_code',
            'ulb_name',
            'application_code',
            'application_name',
            'role_code',
            'role_name',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'End date cannot be earlier than start date.'
            })

        return attrs        