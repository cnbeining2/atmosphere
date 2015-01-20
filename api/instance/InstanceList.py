from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rtwo.exceptions import ConnectionFailure
from libcloud.common.types import InvalidCredsError, MalformedResponseError

from threepio import logger

from core.models.identity import Identity
from core.models.instance import convert_esh_instance
from service.cache import get_cached_instances
from service.driver import prepare_driver
from service.instance import launch_instance
from service.exceptions import OverAllocationError, OverQuotaError, SizeNotAvailable, SecurityGroupNotCreated

from api import failure_response, invalid_creds, connection_failure, malformed_response
from api.permissions import ApiAuthRequired
from api.serializers import InstanceSerializer

from .errors import over_quota, keys_not_found, size_not_availabe


def valid_post_data(data):
    """
    Return any missing required post key names.
    """
    required = ['machine_alias', 'size_alias', 'name']
    #Return any keys that don't match criteria
    return [key for key in required
            #Key must exist and have a non-empty value.
            if key not in data
            or (type(data[key]) == str and len(data[key]) > 0)]


class InstanceList(APIView):
    """
    Instances are the objects created when you launch a machine. They are
    represented by a unique ID, randomly generated on launch, important
    attributes of an Instance are:
    Name, Status (building, active, suspended), Size, Machine"""

    permission_classes = (ApiAuthRequired,)

    def get(self, request, provider_id, identity_id):
        """
        Returns a list of all instances
        """
        user = request.user
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)
        identity = Identity.objects.get(id=identity_id)
        try:
            esh_instance_list = get_cached_instances(identity=identity)
        except MalformedResponseError:
            return malformed_response(provider_id, identity_id)
        except InvalidCredsError:
            return invalid_creds(provider_id, identity_id)
        core_instance_list = [convert_esh_instance(esh_driver,
                                                   inst,
                                                   provider_id,
                                                   identity_id,
                                                   user)
                              for inst in esh_instance_list]
        #TODO: Core/Auth checks for shared instances
        serialized_data = InstanceSerializer(core_instance_list,
                                             context={"request":request},
                                             many=True).data
        response = Response(serialized_data)
        response['Cache-Control'] = 'no-cache'
        return response

    def post(self, request, provider_id, identity_id, format=None):
        """
        Instance Class:
        Launches an instance based on the params
        Returns a single instance

        Parameters: machine_alias, size_alias, username

        TODO: Create a 'reverse' using the instance-id to pass
        the URL for the newly created instance
        I.e: url = "/provider/1/instance/1/i-12345678"
        """
        data = request.DATA
        user = request.user
        #Check the data is valid
        missing_keys = valid_post_data(data)
        if missing_keys:
            return keys_not_found(missing_keys)

        #Pass these as args
        size_alias = data.pop('size_alias')
        machine_alias = data.pop('machine_alias')
        hypervisor_name = data.pop('hypervisor',None)
        try:
            logger.debug(data)
            core_instance = launch_instance(
                user, provider_id, identity_id,
                size_alias, machine_alias,
                ex_availability_zone=hypervisor_name,
                **data)
        except OverQuotaError, oqe:
            return over_quota(oqe)
        except OverAllocationError, oae:
            return over_quota(oae)
        except SizeNotAvailable, snae:
            return size_not_availabe(snae)
        except SecurityGroupNotCreated:
            return connection_failure(provider_id, identity_id)
        except ConnectionFailure:
            return connection_failure(provider_id, identity_id)
        except InvalidCredsError:
            return invalid_creds(provider_id, identity_id)
        except Exception as exc:
            logger.exception("Encountered a generic exception. "
                             "Returning 409-CONFLICT")
            return failure_response(status.HTTP_409_CONFLICT,
                                    str(exc.message))

        serializer = InstanceSerializer(core_instance,
                                        context={"request":request},
                                        data=data)
        #NEVER WRONG
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
