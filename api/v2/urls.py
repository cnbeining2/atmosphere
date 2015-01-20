from django.conf.urls import patterns, include, url
from rest_framework import routers
from api.v2 import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tags', views.TagViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
