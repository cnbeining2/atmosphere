from core.models import Identity
from rest_framework import serializers


class IdentitySerializer(serializers.ModelSerializer):
    quota = serializers.ReadOnlyField(source='get_quota_dict')

    class Meta:
        model = Identity
        fields = ('id', 'quota')
