from rest_framework import viewsets
from core.models import Tag
from core.models.user import AtmosphereUser
from .serializers import TagSerializer, UserSerializer


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
