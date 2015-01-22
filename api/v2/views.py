from rest_framework import viewsets
from core.models import Tag, Project
from core.models.user import AtmosphereUser
from .serializers import TagSerializer, UserSerializer, ProjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = AtmosphereUser.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
