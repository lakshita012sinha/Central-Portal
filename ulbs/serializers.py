from rest_framework import serializers

from .models import ULB, ULBDatabaseConfiguration, ULBApplication


class ULBSerializer(serializers.ModelSerializer):

    class Meta:
        model = ULB

        fields = [
            'id',
            'ulb_code',
            'ulb_name',
            'ulb_type',
            'state',
            'district',
            'city',
            'legal_name',
            'email',
            'phone',
            'address',
            'contact_person',
            'valid_from',
            'valid_to',
            'status',
            'is_active',
            'notes',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):

        valid_from = attrs.get(
            'valid_from',
            getattr(self.instance, 'valid_from', None)
        )

        valid_to = attrs.get(
            'valid_to',
            getattr(self.instance, 'valid_to', None)
        )

        if valid_to and valid_from and valid_to < valid_from:
            raise serializers.ValidationError({
                'valid_to': 'Valid To cannot be earlier than Valid From.'
            })

        return attrs


class ULBDatabaseConfigurationSerializer(serializers.ModelSerializer):

    # Read-only display names
    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    class Meta:
        model = ULBDatabaseConfiguration

        fields = [
            'id',
            'ulb',
            'ulb_name',
            'application',
            'application_name',
            'database_alias',
            'database_name',
            'database_host',
            'database_port',
            'database_username',
            'database_secret_reference',
            'database_engine',
            'ssl_required',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'ulb_name',
            'application_name',
            'created_at',
            'updated_at',
        ]


class ULBApplicationSerializer(serializers.ModelSerializer):

    ulb_name = serializers.CharField(
        source='ulb.ulb_name',
        read_only=True
    )

    application_name = serializers.CharField(
        source='application.application_name',
        read_only=True
    )

    class Meta:
        model = ULBApplication

        fields = [
            'id',
            'ulb',
            'ulb_name',
            'application',
            'application_name',
            'start_date',
            'end_date',
            'status',
            'default_role',
            'remarks',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'ulb_name',
            'application_name',
            'created_at',
            'updated_at',
        ]
