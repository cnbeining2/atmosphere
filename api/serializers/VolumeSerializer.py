from rest_framework import serializers
from .CleanedIdentitySerializer import CleanedIdentitySerializer
from .ProjectsField import ProjectsField
from .get_context_user import get_context_user
from core.models import Volume

class VolumeSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True, source='esh_status')
    attach_data = serializers.Field(source='esh_attach_data')
    #metadata = serializers.Field(source='esh_metadata')
    mount_location = serializers.Field(source='mount_location')
    identity = CleanedIdentitySerializer(source="created_by_identity")
    projects = ProjectsField()

    def __init__(self, *args, **kwargs):
        user = get_context_user(self, kwargs)
        self.request_user = user
        super(VolumeSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Volume
        exclude = ('id', 'created_by_identity', 'end_date')