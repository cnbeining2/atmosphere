from atmosphere.logger import logger
from service.api import getEshDriver, launchEshInstance
from core.models import Identity, ProviderMembership, IdentityMembership,\
                        Provider, Group, UserProfile, Instance, Machine,\
                        ProviderMachine, Credential, Quota, Tag

RUNNER_USERNAME='esteve'
#NOTE: Probably best to run this only on dev regions late at night..
PROVIDERS=['OPENSTACK',]

def run():
    for provider_name in PROVIDERS:
        driver = getEshDriver(
            Identity.objects.get(
                provider__location=provider_name,
                created_by__username=RUNNER_USERNAME),
            RUNNER_USERNAME)
        runnable_machines = [m for m in driver.list_machines()
                             if 'eki' not in m.name
                             and 'eri' not in m.name]
        for idx, m in enumerate(runnable_machines):
            try:
                (token, esh_instance) = launchEshInstance(driver, {
                    'machine_alias': m.alias,
                    'size_alias': '2',
                    'name': 'Testing Deploy and Networking %s' % ((idx + 1), )})
                time.sleep(180)
                #Test the SSH port
                #Test that your key works
                #Test the VNC port
                #etc.
            except Exception as e:
                logger.exception(e)
            finally:
                #driver.destroy_instance(esh_instance.id)
                pass
