"""
Atmosphere service group rest api.

"""

from rest_framework.views import APIView
from rest_framework.response import Response

from threepio import logger


from core.models.group import Group as CoreGroup

from api.permissions import InMaintenance, ApiAuthOptional, ApiAuthRequired
from api.serializers import GroupSerializer

class GroupList(APIView):
    """Every User is assigned to a Group of their own name initially. This
    'usergroup' is then in charge of all the identities, providers, instances,
    and applications which can be shared among other, larger groups, but can
    still be tracked back to the original user who made the API request."""
    permission_classes = (ApiAuthRequired,)

    def post(self, request):
        """Authentication Required, Create a new group.

        Params:name -- The name of the group
               user -- One or more users belonging to the group
        """
        params = request.DATA
        groupname = params['name']
        #STEP1 Create the account on the provider
        group = CoreGroup.objects.create(name=groupname)
        for user in params['user[]']:
                group.user_set.add(user)
        #STEP3 Return the new groups serialized profile
        serialized_data = GroupSerializer(group).data
        response = Response(serialized_data)
        return response

    
    def get(self, request):
        """
        Authentication Required, A list of all the user's groups.
        """
        user = request.user
        all_groups = user.group_set.order_by('name')
        serialized_data = GroupSerializer(all_groups).data
        response = Response(serialized_data)
        return response


class Group(APIView):
    """Every User is assigned to a Group of their own name initially. This
    'usergroup' is then in charge of all the identities, providers, instances,
    and applications which can be shared among other, larger groups, but can
    still be tracked back to the original user who made the API request."""

    permission_classes = (ApiAuthRequired,)

    def get(self, request, groupname):
        """Authentication Required, Retrieve details about a specific group."""
        logger.info(request.__dict__)
        user = request.user
        group = user.group_set.get(name=groupname)
        serialized_data = GroupSerializer(group).data
        response = Response(serialized_data)
        return response
