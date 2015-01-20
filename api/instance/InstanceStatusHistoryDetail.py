from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import AtmosphereUser as User
from core.models.instance import Instance as CoreInstance
from api import failure_response
from api.permissions import ApiAuthRequired
from api.serializers import InstanceStatusHistorySerializer

class InstanceStatusHistoryDetail(APIView):
    """List of instance status history for specific instance."""

    permission_classes = (ApiAuthRequired,)

    def get(self, request, instance_id):
        """
        Authentication required, Retrieve a list of previously launched instances.
        """
        data = request.DATA
        params = request.QUERY_PARAMS.copy()
        user = User.objects.filter(username=request.user)
        if user and len(user) > 0:
            user = user[0]
        else:
            return failure_response(status.HTTP_401_UNAUTHORIZED,
                                    'Request User %s not found' %
                                    user)
        emulate_name = params.pop('username', None)
        # Support for staff users to emulate a specific user history
        if user.is_staff and emulate_name:
            emualate_name = emulate_name[0]  # Querystring conversion
            user = User.objects.filter(username=emulate_name)
            if user and len(user) > 0:
                user = user[0]
            else:
                return failure_response(status.HTTP_401_UNAUTHORIZED,
                                        'Emulated User %s not found' %
                                        emualte_name)
        # List of all instances matching user, instance_id
        core_instance = CoreInstance.objects.filter(
            created_by=user,
            provider_alias=instance_id).order_by("-start_date")
        if core_instance and len(core_instance) > 0:
            core_instance = core_instance[0]
        else:
            return failure_response(status.HTTP_401_UNAUTHORIZED,
                                    'Instance %s not found' %
                                    instance_id)
        status_history = core_instance\
                .instancestatushistory_set.order_by('start_date')
        serialized_data = InstanceStatusHistorySerializer(
                status_history, many=True).data
        response = Response(serialized_data)
        response['Cache-Control'] = 'no-cache'
        return response