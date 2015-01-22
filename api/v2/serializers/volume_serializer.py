from core.models import Volume
from rest_framework import serializers


class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        # fields = ('id',)
