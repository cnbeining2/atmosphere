from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

from threepio import logger


from core.query import only_current, only_current_provider
from core.models.group import Group
from core.models.identity import Identity as CoreIdentity
from core.models.provider import Provider

from api import failure_response, invalid_provider, invalid_provider_identity
from api.serializers import IdentitySerializer, IdentityDetailSerializer
from api.permissions import InMaintenance, ApiAuthRequired

#Shortcuts
def get_provider(user, provider_uuid):
    """
    Given the (request) user and a provider uuid,
    return None or an Active provider
    """
    try:
        group = Group.objects.get(name=user.username)
        provider = group.providers.get(
                #Non-end dated provider
                only_current(),
                #Active provider
                active=True,
                uuid=provider_uuid)
        return provider
    except Group.DoesNotExist:
        logger.warn("Group %s DoesNotExist" % user.username)
        return None
    except Provider.DoesNotExist:
        logger.warn("Provider %s DoesNotExist" % provider_uuid)
        return None

def get_identity_list(user, provider=None):
    """
    Given the (request) user
    return all identities on all active providers
    """
    try:
        group = Group.objects.get(name=user.username)
        if provider:
            identity_list = group.identities.filter(
                provider=provider,
                #Active providers only
                provider__active=True)
        else:
            identity_list = group.identities.filter(
                #Non-end dated providers as search base
                only_current_provider(),
                #Active providers only
                provider__active=True)
        return identity_list
    except Group.DoesNotExist:
        logger.warn("Group %s DoesNotExist" % user.username)
        return None
    except CoreIdentity.DoesNotExist:
        logger.warn("Identity %s DoesNotExist" % identity_uuid)
        return None

def get_identity(user, identity_uuid):
    """
    Given the (request) user and an identity uuid,
    return None or an Active Identity
    """
    try:
        identity_list = get_identity_list(user)
        if not identity_list:
            raise CoreIdentity.DoesNotExist("No identities found for user %s" %
                    user.username)
        identity = identity_list.get(uuid=identity_uuid)
        return identity
    except CoreIdentity.DoesNotExist:
        logger.warn("Identity %s DoesNotExist" % identity_uuid)
        return None

class IdentityDetail(APIView):
    """The identity contains every credential necessary for atmosphere to connect 'The Provider' with a specific user.
    These credentials can vary from provider to provider.
    """

    permission_classes = (ApiAuthRequired,)

    def get(self, request, identity_uuid):
        """
        Authentication Required, all identities available to the user
        """
        identity = get_identity(request.user, identity_uuid)
        if not identity:
            return failure_response(
                status.HTTP_404_NOT_FOUND,
                "The requested Identity ID %s was not found on an active provider"
                % identity_uuid)
        serialized_data = IdentityDetailSerializer(identity).data
        return Response(serialized_data)


class IdentityDetailList(APIView):
    """The identity contains every credential necessary for atmosphere to connect 'The Provider' with a specific user.
    These credentials can vary from provider to provider.
    """

    permission_classes = (ApiAuthRequired,)

    def get(self, request):
        """
        Authentication Required, all identities available to the user
        """
        identities = get_identity_list(request.user)
        serialized_data = IdentityDetailSerializer(identities, many=True).data
        return Response(serialized_data)


class IdentityList(APIView):
    """The identity contains every credential necessary for atmosphere to connect 'The Provider' with a specific user.
    These credentials can vary from provider to provider.
    """

    permission_classes = (ApiAuthRequired,)
    
    def get(self, request, provider_uuid, format=None):
        """
        List of identities for the user on the selected provider.
        """
        provider = get_provider(request.user, provider_uuid)
        if not provider:
            return invalid_provider(provider_uuid)

        identities = get_identity_list(request.user, provider)
        serialized_data = IdentitySerializer(identities, many=True).data
        return Response(serialized_data)


class Identity(APIView):
    """The identity contains every credential necessary for atmosphere to connect 'The Provider' with a specific user.
    These credentials can vary from provider to provider.
    """

    permission_classes = (ApiAuthRequired,)
    
    def get(self, request, provider_uuid, identity_uuid, format=None):
        """
        Authentication Required, Get details for a specific identity.
        """
        provider = get_provider(request.user, provider_uuid)
        identity = get_identity(request.user, identity_uuid)
        if not provider or not identity:
            return invalid_provider_identity(provider_uuid, identity_uuid)
        serialized_data = IdentitySerializer(identity).data
        logger.debug(type(serialized_data))
        return Response(serialized_data)
