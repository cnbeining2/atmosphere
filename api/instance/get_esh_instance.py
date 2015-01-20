from libcloud.common.types import InvalidCredsError, MalformedResponseError
from core.models.instance import Instance as CoreInstance
from service.driver import prepare_driver


def get_esh_instance(request, provider_id, identity_id, instance_id):
    esh_driver = prepare_driver(request, provider_id, identity_id)
    if not esh_driver:
        raise InvalidCredsError(
                "Provider_id && identity_id "
                "did not produce a valid combination")
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
        return esh_instance
    return esh_instance