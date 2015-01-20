from rest_framework import serializers
from core.models.credential import Credential


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        exclude = ('identity',)