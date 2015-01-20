from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models.tag import Tag as CoreTag
from api.permissions import ApiAuthRequired
from api.serializers import TagSerializer
from .get_core_instance import get_core_instance
from .errors import instance_not_found


class InstanceTagList(APIView):
    """
        Tags are a easy way to allow users to group several images as similar
        based on a feature/program of the application.
    """
    permission_classes = (ApiAuthRequired,)

    def get(self, request, provider_id, identity_id, instance_id, *args, **kwargs):
        """
        List all public tags.
        """
        core_instance = get_core_instance(request, provider_id,
                                          identity_id, instance_id)
        if not core_instance:
            instance_not_found(instance_id)
        tags = core_instance.tags.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, provider_id, identity_id, instance_id,
             *args, **kwargs):
        """Create a new tag resource
        Params:name -- Name of the new Tag
        Returns:
        Status Code: 201 Body: A new Tag object
        Status Code: 400 Body: Errors (Duplicate/Invalid Name)
        """
        user = request.user
        data = request.DATA.copy()
        if 'name' not in data:
            return Response("Missing 'name' in POST data",
                    status=status.HTTP_400_BAD_REQUEST)

        core_instance = get_core_instance(request, provider_id, identity_id, instance_id)
        if not core_instance:
            instance_not_found(instance_id)

        created = False
        same_name_tags = CoreTag.objects.filter(name__iexact=data['name'])
        if same_name_tags:
            add_tag = same_name_tags[0]
        else:
            data['user'] = user.username
            data['name'] = data['name'].lower()
            #description is optional
            serializer = TagSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            add_tag = serializer.object
            created = True
        core_instance.tags.add(add_tag)
        return Response(status=status.HTTP_204_NO_CONTENT)