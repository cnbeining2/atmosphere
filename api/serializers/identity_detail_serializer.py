from rest_framework import serializers
from core.models import Identity


class IdentityDetailSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(source='creator_name')
    quota = serializers.ReadOnlyField(source='get_quota_dict')
    provider_id = serializers.ReadOnlyField(source='provider.id')

    class Meta:
        model = Identity
        exclude = ('created_by', 'provider')