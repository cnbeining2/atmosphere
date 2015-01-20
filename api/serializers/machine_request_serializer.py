from rest_framework import serializers
from core.models.machine_request import MachineRequest
# from .new_threshold_field import NewThresholdField

class MachineRequestSerializer(serializers.ModelSerializer):
    """
    """
    instance = serializers.SlugRelatedField(slug_field='provider_alias', read_only=True)
    status = serializers.CharField(default="pending")
    parent_machine = serializers.SlugRelatedField(slug_field='identifier', read_only=True)

    sys = serializers.CharField(default="", source='iplant_sys_files', required=False)
    software = serializers.CharField(default="No software listed", source='installed_software', required=False)
    exclude_files = serializers.CharField(default="", required=False)
    shared_with = serializers.CharField(source="access_list", required=False)

    name = serializers.CharField(source='new_machine_name')
    provider = serializers.PrimaryKeyRelatedField(source='new_machine_provider', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', source='new_machine_owner', read_only=True)
    vis = serializers.CharField(source='new_machine_visibility')
    description = serializers.CharField(source='new_machine_description', required=False)
    tags = serializers.CharField(source='new_machine_tags', required=False)
    # threshold = NewThresholdField(source='new_machine_threshold')
    new_machine = serializers.SlugRelatedField(slug_field='identifier', required=False, read_only=True)

    class Meta:
        model = MachineRequest
        fields = ('id', 'instance', 'status', 'name', 'owner', 'provider',
                  'vis', 'description', 'tags', 'sys', 'software', 'threshold',
                  'shared_with', 'new_machine')