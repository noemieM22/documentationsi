from django.urls import path, include
from api.views import *
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
urlpatterns =  [
    path('article/(?P<bt>[\w]+)',views.URLPathViewSet.as_view(), name ='article'), # fiche déatillée d'un logiciel
    path('article/',views.URLPathViewSet.as_view(), name ='article'), # fiche déatillée d'un logiciel
    path('articlemodule/(?P<bt>[\w]+)',views.URLPathModuleViewSet.as_view(), name ='articlemodule'), # fiche déatillée d'un logiciel
    path('articlemodule/',views.URLPathModuleViewSet.as_view(), name ='articlemodule'), # fiche déatillée d'un logiciel

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',namespace = 'rest_framework'))
]
