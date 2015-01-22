from django.conf.urls import patterns, include, url
from rest_framework import routers
from api.v2 import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'identities', views.IdentityViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
