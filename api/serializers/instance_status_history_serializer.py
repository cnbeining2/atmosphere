from rest_framework import serializers
from core.models import InstanceStatusHistory

class InstanceStatusHistorySerializer(serializers.ModelSerializer):
    instance = serializers.SlugRelatedField(slug_field='provider_alias', read_only=True)
    size = serializers.SlugRelatedField(slug_field='alias', read_only=True)

    class Meta:
        model = InstanceStatusHistory