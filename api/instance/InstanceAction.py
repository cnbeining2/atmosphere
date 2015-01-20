from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rtwo.exceptions import ConnectionFailure
from libcloud.common.types import InvalidCredsError
from threepio import logger
from core.models.volume import convert_esh_volume
from service import task
from service.driver import prepare_driver
from service.instance import redeploy_init, reboot_instance, resize_instance, confirm_resize, start_instance, \
    resume_instance, stop_instance, suspend_instance
from service.exceptions import OverAllocationError, OverQuotaError, SizeNotAvailable, HypervisorCapacityError, \
    VolumeMountConflict
from api import failure_response, invalid_creds, connection_failure
from api.permissions import ApiAuthRequired
from api.serializers import VolumeSerializer
from .errors import over_quota, mount_failed, size_not_availabe, over_capacity


class InstanceAction(APIView):
    """
    This endpoint will allow you to run a specific action on an instance.
    The GET method will retrieve all available actions and any parameters that are required.
    The POST method expects DATA: {"action":...}
                            Returns: 200, data: {'result':'success',...}
                                     On Error, a more specfific message applies.
    Data variables:
     ___
    * action - The action you wish to take on your instance
    * action_params - any parameters required (as detailed on the api) to run the requested action.

    Instances are the objects created when you launch a machine. They are
    represented by a unique ID, randomly generated on launch, important
    attributes of an Instance are:
    Name, Status (building, active, suspended), Size, Machine"""

    permission_classes = (ApiAuthRequired,)

    def get(self, request, provider_id, identity_id, instance_id):
        """Authentication Required, List all available instance actions ,including necessary parameters.
        """
        actions = [{"action":"attach_volume",
                 "action_params":{
                     "volume_id":"required",
                     "device":"optional",
                     "mount_location":"optional"},
                 "description":"Attaches the volume <id> to instance"},
                {"action":"mount_volume",
                 "action_params":{
                     "volume_id":"required",
                     "device":"optional",
                     "mount_location":"optional"
                     },
                 "description":"Unmount the volume <id> from instance"},
                {"action":"unmount_volume",
                 "action_params":{
                     "volume_id":"required",
                     },
                 "description":"Mount the volume <id> to instance"},
                {"action":"detach_volume",
                 "action_params":{"volume_id":"required"},
                 "description":"Detaches the volume <id> to instance"},
                {"action":"resize",
                 "action_params":{"size":"required"},
                 "description":"Resize instance to size <id>"},
                {"action":"confirm_resize",
                 "description":"Confirm the instance works after resize."},
                {"action":"revert_resize",
                 "description":"Revert the instance if resize fails."},
                {"action":"suspend",
                 "description":"Suspend the instance."},
                {"action":"resume",
                 "description":"Resume the instance."},
                {"action":"start",
                 "description":"Start the instance."},
                {"action":"stop",
                 "description":"Stop the instance."},
                {"action":"reboot",
                 "action_params":{"reboot_type (optional)":"SOFT/HARD"},
                 "description":"Stop the instance."},
                {"action":"console",
                 "description":"Get noVNC Console."}]
        response = Response(actions, status=status.HTTP_200_OK)
        return response

    def post(self, request, provider_id, identity_id, instance_id):
        """Authentication Required, Attempt a specific instance action, including necessary parameters.
        """
        #Service-specific call to action
        action_params = request.DATA
        if not action_params.get('action', None):
            return failure_response(
                status.HTTP_400_BAD_REQUEST,
                'POST request to /action require a BODY with \'action\'.')
        result_obj = None
        user = request.user
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)

        esh_instance = esh_driver.get_instance(instance_id)
        if not esh_instance:
            return failure_response(
                status.HTTP_400_BAD_REQUEST,
                'Instance %s no longer exists' % (instance_id,))
        action = action_params['action']
        try:
            if 'volume' in action:
                volume_id = action_params.get('volume_id')
                mount_location = action_params.get('mount_location', None)
                device = action_params.get('device', None)
                if 'attach_volume' == action:
                    if mount_location == 'null' or mount_location == 'None':
                        mount_location = None
                    if device == 'null' or device == 'None':
                        device = None
                    future_mount_location = task.attach_volume_task(esh_driver, esh_instance.alias,
                                            volume_id, device, mount_location)
                elif 'mount_volume' == action:
                    future_mount_location = task.mount_volume_task(esh_driver, esh_instance.alias,
                            volume_id, device, mount_location)
                elif 'unmount_volume' == action:
                    (result, error_msg) = task.unmount_volume_task(esh_driver, esh_instance.alias,
                            volume_id, device, mount_location)
                elif 'detach_volume' == action:
                    (result, error_msg) = task.detach_volume_task(
                        esh_driver,
                        esh_instance.alias,
                        volume_id)
                    if not result and error_msg:
                        #Return reason for failed detachment
                        return failure_response(
                            status.HTTP_400_BAD_REQUEST,
                            error_msg)
                #Task complete, convert the volume and return the object
                esh_volume = esh_driver.get_volume(volume_id)
                core_volume = convert_esh_volume(esh_volume,
                                                 provider_id,
                                                 identity_id,
                                                 user)
                result_obj = VolumeSerializer(core_volume,
                                              context={"request":request}
                                              ).data
            elif 'resize' == action:
                size_alias = action_params.get('size', '')
                if type(size_alias) == int:
                    size_alias = str(size_alias)
                resize_instance(esh_driver, esh_instance, size_alias,
                               provider_id, identity_id, user)
            elif 'confirm_resize' == action:
                confirm_resize(esh_driver, esh_instance,
                               provider_id, identity_id, user)
            elif 'revert_resize' == action:
                esh_driver.revert_resize_instance(esh_instance)
            elif 'redeploy' == action:
                redeploy_init(esh_driver, esh_instance, countdown=None)
            elif 'resume' == action:
                resume_instance(esh_driver, esh_instance,
                                provider_id, identity_id, user)
            elif 'suspend' == action:
                suspend_instance(esh_driver, esh_instance,
                                 provider_id, identity_id, user)
            elif 'start' == action:
                start_instance(esh_driver, esh_instance,
                               provider_id, identity_id, user)
            elif 'stop' == action:
                stop_instance(esh_driver, esh_instance,
                              provider_id, identity_id, user)
            elif 'reset_network' == action:
                esh_driver.reset_network(esh_instance)
            elif 'console' == action:
                result_obj = esh_driver._connection.ex_vnc_console(esh_instance)
            elif 'reboot' == action:
                reboot_type = action_params.get('reboot_type', 'SOFT')
                reboot_instance(esh_driver, esh_instance,
                        identity_id, user, reboot_type)
            elif 'rebuild' == action:
                machine_alias = action_params.get('machine_alias', '')
                machine = esh_driver.get_machine(machine_alias)
                esh_driver.rebuild_instance(esh_instance, machine)
            else:
                return failure_response(
                    status.HTTP_400_BAD_REQUEST,
                    'Unable to to perform action %s.' % (action))
            #ASSERT: The action was executed successfully
            api_response = {
                'result': 'success',
                'message': 'The requested action <%s> was run successfully'
                % action_params['action'],
                'object': result_obj,
            }
            response = Response(api_response, status=status.HTTP_200_OK)
            return response
        ### Exception handling below..
        except HypervisorCapacityError, hce:
            return over_capacity(hce)
        except OverQuotaError, oqe:
            return over_quota(oqe)
        except OverAllocationError, oae:
            return over_quota(oae)
        except SizeNotAvailable, snae:
            return size_not_availabe(snae)
        except ConnectionFailure:
            return connection_failure(provider_id, identity_id)
        except InvalidCredsError:
            return invalid_creds(provider_id, identity_id)
        except VolumeMountConflict, vmc:
            return mount_failed(vmc)
        except NotImplemented, ne:
            return failure_response(
                status.HTTP_404_NOT_FOUND,
                "The requested action %s is not available on this provider"
                % action_params['action'])
        except Exception, exc:
            logger.exception("Exception occurred processing InstanceAction")
            message = exc.message
            if message.startswith('409 Conflict'):
                return failure_response(
                    status.HTTP_409_CONFLICT,
                    message)
            return failure_response(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "The requested action %s encountered "
                "an irrecoverable exception: %s"
                % (action_params['action'], message))
