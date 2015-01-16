from rest_framework import serializers
from core.models import Identity


class IdentitySerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(source='creator_name')
    # credentials = serializers.ReadOnlyField(source='get_credentials')
    quota = serializers.ReadOnlyField(source='get_quota_dict')
    # membership = serializers.ReadOnlyField(source='get_membership')

    class Meta:
        model = Identity
        fields = ('id', 'provider', 'quota')