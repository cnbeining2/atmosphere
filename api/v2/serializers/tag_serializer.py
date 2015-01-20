from core.models import Tag
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Tag
        fields = ('id', 'name', 'description', 'user')
