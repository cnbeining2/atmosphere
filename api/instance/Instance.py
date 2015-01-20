from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import ApiAuthRequired
from service.driver import prepare_driver
from api import failure_response, invalid_creds
from core.models.instance import Instance as CoreInstance
from .errors import instance_not_found
from core.models.instance import convert_esh_instance
from api.serializers import InstanceSerializer
from threepio import logger
from service.instance import update_instance_metadata, _check_volume_attachment
from service import task
from service.cache import invalidate_cached_instances
from core.models.identity import Identity
from rest_framework import status
from service.exceptions import VolumeAttachConflict
from rtwo.exceptions import ConnectionFailure
from libcloud.common.types import InvalidCredsError
from api import connection_failure


class Instance(APIView):
    """
    Instances are the objects created when you launch a machine. They are
    represented by a unique ID, randomly generated on launch, important
    attributes of an Instance are:
    Name, Status (building, active, suspended), Size, Machine"""
    #renderer_classes = (JSONRenderer, JSONPRenderer)

    permission_classes = (ApiAuthRequired,)

    def get(self, request, provider_id, identity_id, instance_id):
        """
        Authentication Required, get instance details.
        """
        user = request.user
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)
        esh_instance = esh_driver.get_instance(instance_id)
        if not esh_instance:
            try:
                core_inst = CoreInstance.objects.get(
                    provider_alias=instance_id,
                    provider_machine__provider__id=provider_id,
                    created_by_identity__id=identity_id)
                core_inst.end_date_all()
            except CoreInstance.DoesNotExist:
                pass
            return instance_not_found(instance_id)
        core_instance = convert_esh_instance(esh_driver, esh_instance,
                                             provider_id, identity_id, user)
        serialized_data = InstanceSerializer(core_instance,
                                             context={"request":request}).data
        response = Response(serialized_data)
        response['Cache-Control'] = 'no-cache'
        return response

    def patch(self, request, provider_id, identity_id, instance_id):
        """Authentication Required, update metadata about the instance"""
        user = request.user
        data = request.DATA
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)
        esh_instance = esh_driver.get_instance(instance_id)
        if not esh_instance:
            return instance_not_found(instance_id)
        #Gather the DB related item and update
        core_instance = convert_esh_instance(esh_driver, esh_instance,
                                             provider_id, identity_id, user)
        serializer = InstanceSerializer(core_instance, data=data,
                                        context={"request":request}, partial=True)
        if serializer.is_valid():
            logger.info('metadata = %s' % data)
            update_instance_metadata(esh_driver, esh_instance, data,
                    replace=False)
            serializer.save()
            invalidate_cached_instances(identity=Identity.objects.get(id=identity_id))
            response = Response(serializer.data)
            logger.info('data = %s' % serializer.data)
            response['Cache-Control'] = 'no-cache'
            return response
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, provider_id, identity_id, instance_id):
        """Authentication Required, update metadata about the instance"""
        user = request.user
        data = request.DATA
        #Ensure item exists on the server first
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)
        esh_instance = esh_driver.get_instance(instance_id)
        if not esh_instance:
            return instance_not_found(instance_id)
        #Gather the DB related item and update
        core_instance = convert_esh_instance(esh_driver, esh_instance,
                                             provider_id, identity_id, user)
        serializer = InstanceSerializer(core_instance, data=data,
                                        context={"request":request})
        if serializer.is_valid():
            logger.info('metadata = %s' % data)
            update_instance_metadata(esh_driver, esh_instance, data)
            serializer.save()
            invalidate_cached_instances(identity=Identity.objects.get(id=identity_id))
            response = Response(serializer.data)
            logger.info('data = %s' % serializer.data)
            response['Cache-Control'] = 'no-cache'
            return response
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, provider_id, identity_id, instance_id):
        """Authentication Required, TERMINATE the instance.

        Be careful, there is no going back once you've deleted an instance.
        """
        user = request.user
        esh_driver = prepare_driver(request, provider_id, identity_id)
        if not esh_driver:
            return invalid_creds(provider_id, identity_id)
        try:
            esh_instance = esh_driver.get_instance(instance_id)
            if not esh_instance:
                return instance_not_found(instance_id)
            #Test that there is not an attached volume BEFORE we destroy
            _check_volume_attachment(esh_driver, esh_instance)
            task.destroy_instance_task(esh_instance, identity_id)
            invalidate_cached_instances(identity=Identity.objects.get(id=identity_id))
            existing_instance = esh_driver.get_instance(instance_id)
            if existing_instance:
                #Instance will be deleted soon...
                esh_instance = existing_instance
                if esh_instance.extra\
                   and 'task' not in esh_instance.extra:
                    esh_instance.extra['task'] = 'queueing delete'
            core_instance = convert_esh_instance(esh_driver, esh_instance,
                                                 provider_id, identity_id,
                                                 user)
            if core_instance:
                core_instance.end_date_all()
            else:
                logger.warn("Unable to find core instance %s." % (instance_id))
            serialized_data = InstanceSerializer(core_instance,
                                                 context={"request":request}).data
            response = Response(serialized_data, status=status.HTTP_200_OK)
            response['Cache-Control'] = 'no-cache'
            return response
        except (Identity.DoesNotExist) as exc:
            return failure_response(status.HTTP_400_BAD_REQUEST,
                                    "Invalid provider_id or identity_id.")
        except VolumeAttachConflict as exc:
            message = exc.message
            return failure_response(status.HTTP_409_CONFLICT, message)
        except ConnectionFailure:
            return connection_failure(provider_id, identity_id)
        except InvalidCredsError:
            return invalid_creds(provider_id, identity_id)