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


# # Custom Fields


# class NewThresholdField(serializers.WritableField):
#
#     def to_native(self, threshold_dict):
#         return threshold_dict
#
#     def field_from_native(self, data, files, field_name, into):
#         value = data.get(field_name)
#         if value is None:
#             return
#         memory = value.get('memory',0)
#         disk = value.get('disk',0)
#         machine_request = self.root.object
#         machine_request.new_machine_memory_min = memory
#         machine_request.new_machine_storage_min = disk
#         into[field_name] = value


# class AppBookmarkField(serializers.WritableField):
#
#     def to_native(self, bookmark_mgr):
#         request_user = self.root.request_user
#         if type(request_user) == AnonymousUser:
#             return False
#         try:
#             bookmark_mgr.get(user=request_user)
#             return True
#         except ApplicationBookmark.DoesNotExist:
#             return False
#
#     def field_from_native(self, data, files, field_name, into):
#         value = data.get(field_name)
#         if value is None:
#             return
#         app = self.root.object
#         user = self.root.request_user
#         if value:
#             ApplicationBookmark.objects.\
#                 get_or_create(application=app, user=user)
#             result = True
#         else:
#             ApplicationBookmark.objects\
#                                .filter(application=app, user=user).delete()
#             result = False
#         into[field_name] = result


# class IdentityRelatedField(serializers.RelatedField):
#
#     def to_native(self, identity):
#         quota_dict = identity.get_quota_dict()
#         return {
#             "id": identity.id,
#             "provider": identity.provider.location,
#             "provider_id": identity.provider.id,
#             "quota": quota_dict,
#         }
#
#     def field_from_native(self, data, files, field_name, into):
#         value = data.get(field_name)
#         if value is None:
#             return
#         try:
#             into[field_name] = Identity.objects.get(id=value)
#         except Identity.DoesNotExist:
#             into[field_name] = None


# class InstanceRelatedField(serializers.RelatedField):
#     def to_native(self, instance_alias):
#         instance = Instance.objects.get(provider_alias=instance_alias)
#         return instance.provider_alias
#
#     def field_from_native(self, data, files, field_name, into):
#         value = data.get(field_name)
#         if value is None:
#             return
#         try:
#             into["instance"] = Instance.objects.get(provider_alias=value)
#             into[field_name] = Instance.objects.get(
#                 provider_alias=value).provider_alias
#         except Instance.DoesNotExist:
#             into[field_name] = None


# # Serializers
# class AccountSerializer(serializers.Serializer):
#     pass
#     #Define fields here
#     #TODO: Define a spec that we expect from list_users across all providers


# class ApplicationSerializer(serializers.ModelSerializer):
#     """
#     test maybe something
#     """
#     #Read-Only Fields
#     uuid = serializers.CharField(read_only=True)
#     icon = serializers.CharField(read_only=True, source='icon_url')
#     created_by = serializers.SlugRelatedField(slug_field='username',
#                                               source='created_by',
#                                               read_only=True)
#     #scores = serializers.Field(source='get_scores')
#     uuid_hash = serializers.CharField(read_only=True, source='hash_uuid')
#     #Writeable Fields
#     name = serializers.CharField(source='name')
#     tags = serializers.CharField(source='tags.all')
#     description = serializers.CharField(source='description')
#     start_date = serializers.CharField(source='start_date')
#     end_date = serializers.CharField(source='end_date',
#                                      required=False, read_only=True)
#     private = serializers.BooleanField(source='private')
#     featured = serializers.BooleanField(source='featured')
#     machines = serializers.SerializerMethodField('get_machines')
#     is_bookmarked = AppBookmarkField(source="bookmarks.all")
#     threshold = serializers.RelatedField(read_only=True, source="threshold")
#     projects = ProjectsField()
#
#     def get_machines(self, application):
#         machines = application._current_machines(request_user=self.request_user)
#         return [{"start_date": pm.start_date,
#                  "end_date": pm.end_date,
#                  "alias": pm.identifier,
#                  "version": pm.version,
#                  "provider": pm.provider.id} for pm in machines]
#
#
#     def __init__(self, *args, **kwargs):
#         user = get_context_user(self, kwargs)
#         self.request_user = user
#         super(ApplicationSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = Application


# class PaginatedApplicationSerializer(pagination.PaginationSerializer):
#     """
#     Serializes page objects of Instance querysets.
#     """
#
#     def __init__(self, *args, **kwargs):
#         user = get_context_user(self, kwargs)
#         self.request_user = user
#         super(PaginatedApplicationSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         object_serializer_class = ApplicationSerializer


# class ApplicationBookmarkSerializer(serializers.ModelSerializer):
#     """
#     """
#     #TODO:Need to validate provider/identity membership on id change
#     type = serializers.SerializerMethodField('get_bookmark_type')
#     alias = serializers.SerializerMethodField('get_bookmark_alias')
#
#     def get_bookmark_type(self, bookmark_obj):
#         return "Application"
#
#     def get_bookmark_alias(self, bookmark_obj):
#         return bookmark_obj.application.uuid
#
#     class Meta:
#         model = ApplicationBookmark
#         fields = ('type', 'alias')


# class ApplicationScoreSerializer(serializers.ModelSerializer):
#     """
#     """
#     #TODO:Need to validate provider/identity membership on id change
#     username = serializers.CharField(read_only=True, source='user.username')
#     application = serializers.CharField(read_only=True,
#                                         source='application.name')
#     vote = serializers.CharField(read_only=True, source='get_vote_name')
#
#     class Meta:
#         model = ApplicationScore
#         fields = ('username', "application", "vote")


# class CredentialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Credential
#         exclude = ('identity',)


# class InstanceHistorySerializer(serializers.ModelSerializer):
#     #R/O Fields first!
#     alias = serializers.CharField(read_only=True, source='provider_alias')
#     alias_hash = serializers.CharField(read_only=True, source='hash_alias')
#     created_by = serializers.SlugRelatedField(slug_field='username',
#                                               source='created_by',
#                                               read_only=True)
#     size_alias = serializers.CharField(read_only=True, source='esh_size')
#     machine_alias = serializers.CharField(read_only=True, source='esh_machine')
#     machine_name = serializers.CharField(read_only=True,
#                                          source='esh_machine_name')
#     machine_alias_hash = serializers.CharField(read_only=True,
#                                                source='hash_machine_alias')
#     ip_address = serializers.CharField(read_only=True)
#     start_date = serializers.DateTimeField(read_only=True)
#     end_date = serializers.DateTimeField(read_only=True)
#     provider = serializers.CharField(read_only=True, source='provider_name')
#     #Writeable fields
#     name = serializers.CharField()
#     tags = TagRelatedField(slug_field='name', source='tags', many=True)
#
#     class Meta:
#         model = Instance
#         exclude = ('id', 'provider_machine', 'provider_alias',
#                    'shell', 'vnc', 'created_by_identity')


# class PaginatedInstanceHistorySerializer(pagination.PaginationSerializer):
#     """
#     Serializes page objects of Instance querysets.
#     """
#     class Meta:
#         object_serializer_class = InstanceHistorySerializer


# class PaginatedInstanceSerializer(pagination.PaginationSerializer):
#     """
#     Serializes page objects of Instance querysets.
#     """
#     class Meta:
#         object_serializer_class = InstanceSerializer


# class MachineExportSerializer(serializers.ModelSerializer):
#     """
#     """
#     name = serializers.CharField(source='export_name')
#     instance = serializers.SlugRelatedField(slug_field='provider_alias')
#     status = serializers.CharField(default="pending")
#     disk_format = serializers.CharField(source='export_format')
#     owner = serializers.SlugRelatedField(slug_field='username',
#                                          source='export_owner')
#     file = serializers.CharField(read_only=True, default="",
#                                  required=False, source='export_file')
#
#     class Meta:
#         model = MachineExport
#         fields = ('id', 'instance', 'status', 'name',
#                   'owner', 'disk_format', 'file')


# class MachineRequestSerializer(serializers.ModelSerializer):
#     """
#     """
#     instance = serializers.SlugRelatedField(slug_field='provider_alias')
#     status = serializers.CharField(default="pending")
#     parent_machine = serializers.SlugRelatedField(slug_field='identifier',
#                                                   read_only=True)
#
#     sys = serializers.CharField(default="", source='iplant_sys_files',
#                                 required=False)
#     software = serializers.CharField(default="No software listed",
#                                      source='installed_software',
#                                      required=False)
#     exclude_files = serializers.CharField(default="", required=False)
#     shared_with = serializers.CharField(source="access_list", required=False)
#
#     name = serializers.CharField(source='new_machine_name')
#     provider = serializers.PrimaryKeyRelatedField(
#         source='new_machine_provider')
#     owner = serializers.SlugRelatedField(slug_field='username',
#                                          source='new_machine_owner')
#     vis = serializers.CharField(source='new_machine_visibility')
#     description = serializers.CharField(source='new_machine_description',
#                                         required=False)
#     tags = serializers.CharField(source='new_machine_tags', required=False)
#     threshold = NewThresholdField(source='new_machine_threshold')
#     new_machine = serializers.SlugRelatedField(slug_field='identifier',
#                                                required=False)
#
#     class Meta:
#         model = MachineRequest
#         fields = ('id', 'instance', 'status', 'name', 'owner', 'provider',
#                   'vis', 'description', 'tags', 'sys', 'software', 'threshold',
#                   'shared_with', 'new_machine')