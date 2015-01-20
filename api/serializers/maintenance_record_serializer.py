from rest_framework import serializers
from core.models import MaintenanceRecord


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    provider_id = serializers.ReadOnlyField(source='provider.id')

    class Meta:
        model = MaintenanceRecord
        exclude = ('provider',)