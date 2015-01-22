from core.models import Instance
from rest_framework import serializers


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ('id', 'name', 'ip_address', 'shell', 'vnc', 'start_date')
