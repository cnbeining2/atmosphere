from core.models import Tag
from rest_framework import serializers
from .user_serializer import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username'
    # )

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    user = UserSerializer()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'description', 'user')
