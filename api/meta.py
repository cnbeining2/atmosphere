"""
Atmosphere service meta rest api.

"""
from datetime import datetime
import time

from libcloud.common.types import InvalidCredsError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from threepio import logger

from service.driver import prepare_driver

from api import failure_response, invalid_creds
from api.permissions import InMaintenance, ApiAuthRequired


class Meta(APIView):
    """
    Meta-details about Atmosphere API, including self-describing URLs.
    """
    permission_classes = (ApiAuthRequired,)

    def get(self, request, provider_uuid, identity_uuid):
        """
        Returns all available URLs based on the user profile.
        """
        esh_driver = prepare_driver(request, provider_uuid, identity_uuid)
        if not esh_driver:
            return invalid_creds(provider_uuid, identity_uuid)
        data = add_user_urls(request, provider_uuid, identity_uuid)
        if request.user.is_staff:
            add_staff_urls(request, provider_uuid, identity_uuid)
        return Response(data)


def add_staff_urls(request, provider_uuid, identity_uuid):
    data = {
            'request-image-list': reverse('api:private_apis:direct-machine-request-list',
                            request=request),
        }
def add_user_urls(request, provider_uuid, identity_uuid):
    data = {
        'group-list': reverse('api:public_apis:group-list',
                            request=request),
        'tag-list': reverse('api:public_apis:tag-list',
                            request=request),
        'provider-list': reverse('api:public_apis:provider-list',
                            request=request),
        'occupancy': reverse('api:private_apis:occupancy',
                            args=(provider_uuid,),
                            request=request),
        'hypervisor': reverse('api:private_apis:hypervisor',
                            args=(provider_uuid,),
                            request=request),
        'identity-list': reverse('api:public_apis:identity-list',
                            args=(provider_uuid,),
                            request=request),
        'volume-list': reverse('api:public_apis:volume-list',
                          args=(provider_uuid, identity_uuid),
                          request=request),
        'meta': reverse('api:private_apis:meta-detail',
                        args=(provider_uuid, identity_uuid),
                        request=request),
        'machine-history-list': reverse('api:public_apis:machine-history',
                            args=(provider_uuid, identity_uuid),
                            request=request),
        'instance-history-list': reverse('api:public_apis:instance-history',
                            args=(provider_uuid, identity_uuid),
                            request=request),
        'instance-list': reverse('api:public_apis:instance-list',
                            args=(provider_uuid, identity_uuid),
                            request=request),
        'machine-list': reverse('api:public_apis:machine-list',
                           args=(provider_uuid, identity_uuid),
                           request=request),
        'size-list': reverse('api:public_apis:size-list',
                        args=(provider_uuid, identity_uuid),
                        request=request),
        'profile': reverse('api:public_apis:profile', request=request)
    }
    return data

class MetaAction(APIView):
    """
    Atmosphere service meta rest api.
    """
    permission_classes = (ApiAuthRequired,)
    
    def get(self, request, provider_uuid, identity_uuid, action=None):
        """
        """
        if not action:
            return failure_response(
                status.HTTP_400_BAD_REQUEST,
                'Action is not supported.'
            )
        esh_driver = prepare_driver(request, provider_uuid, identity_uuid)
        if not esh_driver:
            return invalid_creds(provider_uuid, identity_uuid)
        esh_meta = esh_driver.meta()
        try:
            if 'test_links' in action:
                test_links = esh_meta.test_links()
                return Response(test_links, status=status.HTTP_200_OK)
        except InvalidCredsError:
            logger.warn('Authentication Failed. Provider-id:%s Identity-id:%s'
                        % (provider_uuid, identity_uuid))
            return failure_response(
                status.HTTP_401_UNAUTHORIZED,
                'Identity/Provider Authentication Failed')
        except NotImplemented, ne:
            logger.exception(ne)
            return failure_response(
                status.HTTP_404_NOT_FOUND,
                'The requested resource %s is not available on this provider'
                % action)
