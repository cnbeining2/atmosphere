from core.models.instance import convert_esh_instance
from service.driver import prepare_driver
from .get_esh_instance import get_esh_instance


def get_core_instance(request, provider_id, identity_id, instance_id):
    user = request.user
    esh_driver = prepare_driver(request, provider_id, identity_id)
    esh_instance = get_esh_instance(request, provider_id, identity_id, instance_id)
    core_instance = convert_esh_instance(esh_driver, esh_instance,
                                         provider_id, identity_id, user)
    return core_instance