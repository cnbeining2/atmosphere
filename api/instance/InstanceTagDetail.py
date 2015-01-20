from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models.tag import Tag as CoreTag
from api import failure_response
from api.permissions import ApiAuthRequired
from api.serializers import TagSerializer
from .get_core_instance import get_core_instance
from .errors import instance_not_found


class InstanceTagDetail(APIView):
    """
        Tags are a easy way to allow users to group several images as similar
        based on a feature/program of the application.

        This API resource allows you to Retrieve, Update, or Delete your Tag.
    """
    permission_classes = (ApiAuthRequired,)

    def delete(self, request, provider_id, identity_id, instance_id,  tag_slug, *args, **kwargs):
        """
        Remove the tag, if it is no longer in use.
        """
        core_instance = get_core_instance(request, provider_id, identity_id, instance_id)
        if not core_instance:
            instance_not_found(instance_id)
        try:
            tag = core_instance.tags.get(name__iexact=tag_slug)
        except CoreTag.DoesNotExist:
            return failure_response(status.HTTP_404_NOT_FOUND,
                                    'Tag %s not found on instance' % tag_slug)
        core_instance.tags.remove(tag)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, provider_id, identity_id, instance_id,  tag_slug, *args, **kwargs):
        """
        Return the credential information for this tag
        """
        core_instance = get_core_instance(request, provider_id, identity_id, instance_id)
        if not core_instance:
            instance_not_found(instance_id)
        try:
            tag = core_instance.tags.get(name__iexact=tag_slug)
        except CoreTag.DoesNotExist:
            return Response(['Tag does not exist'],
                            status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag)
        return Response(serializer.data)