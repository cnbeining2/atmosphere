from rest_framework import serializers
from core.models import InstanceStatusHistory

class InstanceStatusHistorySerializer(serializers.ModelSerializer):
    instance = serializers.SlugRelatedField(slug_field='provider_alias')
    size = serializers.SlugRelatedField(slug_field='alias')

    class Meta:
        model = InstanceStatusHistory