from api import failure_response
from rest_framework import status


def keys_not_found(missing_keys):
    return failure_response(
        status.HTTP_400_BAD_REQUEST,
        'Missing data for variable(s): %s' % missing_keys)


def instance_not_found(instance_id):
    return failure_response(
        status.HTTP_404_NOT_FOUND,
        'Instance %s does not exist' % instance_id)


def size_not_availabe(sna_exception):
    return failure_response(
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        sna_exception.message)


def over_capacity(capacity_exception):
    return failure_response(
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        capacity_exception.message)


def over_quota(quota_exception):
    return failure_response(
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        quota_exception.message)


def mount_failed(exception):
    return failure_response(
        status.HTTP_409_CONFLICT,
        exception.message)


def over_allocation(allocation_exception):
    return failure_response(
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        allocation_exception.message)