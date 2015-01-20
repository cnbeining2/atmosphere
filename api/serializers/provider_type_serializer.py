from rest_framework import serializers
from core.models import ProviderType

class ProviderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderType