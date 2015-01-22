from rest_framework import viewsets
from core.models import Tag, Project, Application as Image, Provider, Identity, Quota
from core.models.user import AtmosphereUser
from .serializers import TagSerializer, UserSerializer, ProjectSerializer, ImageSerializer, ProviderSerializer, \
    IdentitySerializer, QuotaSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AtmosphereUser.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_fields = ('created_by__username', 'tags__name')
    search_fields = ('name', 'description')


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class IdentityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


class QuotaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer

