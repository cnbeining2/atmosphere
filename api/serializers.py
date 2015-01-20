# from django.contrib.auth.models import AnonymousUser
# from core.models.application import Application, ApplicationScore, ApplicationBookmark, ApplicationThreshold
# from core.models.credential import Credential
# from core.models.group import get_user_group
# from core.models.group import Group
# from core.models.group import IdentityMembership
# from core.models.identity import Identity
# from core.models.instance import Instance
# from core.models.instance import InstanceStatusHistory
# from core.models.machine import ProviderMachine
# from core.models.machine_request import MachineRequest
# from core.models.machine_export import MachineExport
# from core.models.maintenance import MaintenanceRecord
# from core.models.profile import UserProfile
# from core.models.project import Project
# from core.models.provider import ProviderType, Provider
# from core.models.size import Size
# from core.models.step import Step
# from core.models.tag import Tag, find_or_create_tag
# from core.models.user import AtmosphereUser
# from core.models.volume import Volume
# from core.query import only_current
# from rest_framework import serializers
# from rest_framework import pagination
# from threepio import logger


# Useful Serializer methods


# def get_projects_for_obj(serializer, related_obj):
#     """
#     Using <>Serializer.request_user, find the projects
#     the related object is a member of
#     """
#     if not serializer.request_user:
#         return None
#     projects = related_obj.get_projects(serializer.request_user)
#     return [p.id for p in projects]
