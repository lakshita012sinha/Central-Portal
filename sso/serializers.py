from rest_framework import serializers

from .models import SSOClient, SSOAuthorizationCode


class SSOClientSerializer(serializers.ModelSerializer):

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    class Meta:
        model = SSOClient

        fields = [
            'id',
            'application',
            'application_name',
            'client_id',
            'client_secret',
            'audience',
            'issuer',
            'allowed_redirect_uri',
            'code_expiry_seconds',
            'environment',
            'token_method',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'application_name',
            'created_at',
            'updated_at',
        ]


class SSOAuthorizationCodeSerializer(serializers.ModelSerializer):

    client_name = serializers.SerializerMethodField()
    username    = serializers.CharField(source='user.username',  read_only=True)
    ulb_name    = serializers.CharField(source='ulb.ulb_name',   read_only=True)
    is_used     = serializers.SerializerMethodField()
    is_expired  = serializers.SerializerMethodField()

    class Meta:
        model  = SSOAuthorizationCode
        fields = [
            'id',
            'code',
            'client',
            'client_name',
            'user',
            'username',
            'ulb',
            'ulb_name',
            'redirect_uri',
            'expires_at',
            'used_at',
            'created_at',
            'is_used',
            'is_expired',
        ]
        read_only_fields = fields  # authorization codes are created by the SSO flow only

    def get_client_name(self, obj):
        return obj.client.application.application_name if obj.client else '—'

    def get_is_used(self, obj):
        return obj.used_at is not None

    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expires_at < timezone.now()
