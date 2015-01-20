from rest_framework import serializers
from core.models.machine_export import MachineExport


class MachineExportSerializer(serializers.ModelSerializer):
    """
    """
    name = serializers.CharField(source='export_name')
    instance = serializers.SlugRelatedField(slug_field='provider_alias', read_only=True)
    status = serializers.CharField(default="pending")
    disk_format = serializers.CharField(source='export_format')
    owner = serializers.SlugRelatedField(slug_field='username', source='export_owner', read_only=True)
    file = serializers.CharField(read_only=True, default="", required=False, source='export_file')

    class Meta:
        model = MachineExport
        fields = ('id', 'instance', 'status', 'name', 'owner', 'disk_format', 'file')