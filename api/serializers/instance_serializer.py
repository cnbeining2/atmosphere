from rest_framework import serializers
from .cleaned_identity_serializer import CleanedIdentitySerializer
from .tag_related_field import TagRelatedField
from .get_context_user import get_context_user
# from .projects_field import ProjectsField
from core.models import Instance


class InstanceSerializer(serializers.ModelSerializer):
    #R/O Fields first!
    alias = serializers.CharField(read_only=True, source='provider_alias')
    alias_hash = serializers.CharField(read_only=True, source='hash_alias')
    application_name = serializers.CharField(
        read_only=True, source='provider_machine.application.name')
    application_uuid = serializers.CharField(
        read_only=True, source='provider_machine.application.uuid')
    #created_by = serializers.CharField(read_only=True, source='creator_name')
    created_by = serializers.SlugRelatedField(slug_field='username',
                                              source='created_by',
                                              read_only=True)
    status = serializers.CharField(read_only=True, source='esh_status')
    fault = serializers.Field(source='esh_fault')
    size_alias = serializers.CharField(read_only=True, source='esh_size')
    machine_alias = serializers.CharField(read_only=True, source='esh_machine')
    machine_name = serializers.CharField(read_only=True,
                                         source='esh_machine_name')
    machine_alias_hash = serializers.CharField(read_only=True,
                                               source='hash_machine_alias')
    ip_address = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    token = serializers.CharField(read_only=True)
    has_shell = serializers.BooleanField(read_only=True, source='shell')
    has_vnc = serializers.BooleanField(read_only=True, source='vnc')
    identity = CleanedIdentitySerializer(source="created_by_identity",
                                         read_only=True)
    #Writeable fields
    name = serializers.CharField()
    tags = TagRelatedField(slug_field='name', source='tags', many=True, read_only=True)
    # projects = ProjectsField()

    def __init__(self, *args, **kwargs):
        user = get_context_user(self, kwargs)
        self.request_user = user
        super(InstanceSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Instance
        exclude = ('id', 'provider_machine', 'provider_alias',
                   'shell', 'vnc', 'password', 'created_by_identity')
