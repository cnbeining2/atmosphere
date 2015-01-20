from rest_framework import serializers
from core.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    location = serializers.CharField(source='get_location')
    #membership = serializers.Field(source='get_membership')

    class Meta:
        model = Provider
        exclude = ('active', 'start_date', 'end_date')