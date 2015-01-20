from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.permissions import ApiAuthRequired
from core.models import AtmosphereUser as User
from api import failure_response, invalid_creds, connection_failure, malformed_response
from core.models.instance import Instance as CoreInstance
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.serializers import PaginatedInstanceHistorySerializer


def _filter_instance_history(history_instance_list, params):
    #Filter the list based on query strings
    for filter_key, value in params.items():
        if 'start_date' == filter_key:
            history_instance_list = history_instance_list.filter(
                start_date__gt=value)
        elif 'end_date' == filter_key:
            history_instance_list = history_instance_list.filter(
                Q(end_date=None) |
                Q(end_date__lt=value))
        elif 'ip_address' == filter_key:
            history_instance_list = history_instance_list.filter(
                ip_address__contains=value)
        elif 'alias' == filter_key:
            history_instance_list = history_instance_list.filter(
                provider_alias__contains=value)
    return history_instance_list


def _sort_instance_history(history_instance_list, sort_by, descending=False):
    #Using the 'sort_by' variable, sort the list:
    if not sort_by or 'end_date' in sort_by:
        return sorted(history_instance_list, key=lambda ish:
                ish.end_date if ish.end_date else timezone.now(),
                reverse=descending)
    elif 'start_date' in sort_by:
        return sorted(history_instance_list, key=lambda ish:
                ish.start_date if ish.start_date else timezone.now(),
                reverse=descending)


class InstanceHistory(APIView):
    """Paginated list of all instance history for specific user."""

    permission_classes = (ApiAuthRequired,)

    def get(self, request):
        """
        Authentication required, Retrieve a list of previously launched instances.
        """
        data = request.DATA
        params = request.QUERY_PARAMS.copy()
        emulate_name = params.pop('username', None)
        user = request.user
        # Support for staff users to emulate a specific user history
        if user.is_staff and emulate_name:
            emualate_name = emulate_name[0]  # Querystring conversion
            try:
                user = User.objects.get(username=emulate_name)
            except User.DoesNotExist:
                return failure_response(status.HTTP_401_UNAUTHORIZED,
                                        'Emulated User %s not found' %
                                        emualte_name)
        try:
            # List of all instances created by user
            sort_by = params.get('sort_by','')
            order_by = params.get('order_by','desc')
            history_instance_list = CoreInstance.objects.filter(
                created_by=user).order_by("-start_date")
            history_instance_list = _filter_instance_history(
                    history_instance_list, params)
            history_instance_list = _sort_instance_history(
                    history_instance_list, sort_by, 'desc' in order_by.lower())
        except Exception as e:
            return failure_response(
                status.HTTP_400_BAD_REQUEST,
                'Bad query string caused filter validation errors : %s'
                % (e,))

        page = params.get('page')
        if page or len(history_instance_list) == 0:
            paginator = Paginator(history_instance_list, 20,
                                  allow_empty_first_page=True)
        else:
            paginator = Paginator(history_instance_list,
                                  len(history_instance_list),
                                  allow_empty_first_page=True)
        try:
            history_instance_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            history_instance_page = paginator.page(1)
        except EmptyPage:
            # Page is out of range.
            # deliver last page of results.
            history_instance_page = paginator.page(paginator.num_pages)
        serialized_data = PaginatedInstanceHistorySerializer(
                history_instance_page, context={'request':request}).data
        response = Response(serialized_data)
        response['Cache-Control'] = 'no-cache'
        return response