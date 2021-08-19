from django.shortcuts import render,redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

import django_filters.rest_framework

from wiki.models.urlpath import URLPath, Article
from django.contrib.auth.models import Group
from wiki.models.article import *
from api.serializers import *

from django.http import HttpResponse

"""
Utility function:
Creates a new urlpath with an article and a new revision for the
article from an get request

:returns: None (this need to be improve...)

Before use:
copy the file documentation/api/urlpath_ToOverride.py in the prject wiki directly (not in this projet!!!) : wiki/models and rename in urlpath.py
"""

# Création de la structure de Documentation pour un Logiciel:
# Logiciel
#   - Doc (doc user)
#      - Astuces
#   - T'Doc (doc technique)
#      - Installation et MAJ
#      - Debugs
#      - Astuces
class URLPathViewSet(View):
    def get(self,request):

        title =request.GET.get('logiciel')
        slug = title.lower().replace('&','').replace(' ','-')

        # création d'un groupe (qui comprendra acteurs GSI + ref métier)
        groupename = title.replace(' ','-').lower()
        groupenameT = groupename + '_tech'
        group = Group.objects.create(name=groupename)
        groupT = Group.objects.create(name=groupenameT)

        # Objets wiki nécessaires à la création des sous-pages logiciels
        ArticleLogiciel = Article.objects.get(id=5)
        URLPathLogiciel = URLPath.objects.get(id=5)
        # Création de la page Logiciel
        articleLog , newpathLog = URLPath._create_urlpath_from_request_fromotherProject(
            request, ArticleLogiciel, URLPathLogiciel, slug, title, '', '',)
        # Attributs pages à créer à la création d'un logiciel
        titleSlug ={}
        titleSlug["Doc"]="doc"
        titleSlug["Astuces"]="astuces"
        titleSlug["T'Doc"]="tdoc"
        titleSlug["Installation & MAJ"]="installation-maj"
        titleSlug["Debugs"]="debugs"
        pagesToCreate = {}
        pagesToCreate["Doc"] = ["Astuces"]
        pagesToCreate["T'Doc"] = ["Installation & MAJ","Debugs","Astuces"]
        # on envoie une requête à models.urlPaths.py:
        # - méthode _create_urlpath_from_request
        # - paramètres : cls, request, perm_article, parent_urlpath, slug, title, content, summary

        for pages in pagesToCreate:

            article,newpath = URLPath._create_urlpath_from_request_fromotherProject(
                request, articleLog, newpathLog, titleSlug[pages], pages, '', '',)
            if(pages == 'Doc'):
                grantAcces(article,group.id,1,1,1,0)
                for p in pagesToCreate[pages]:
                    art,npath = URLPath._create_urlpath_from_request_fromotherProject(
                        request, article, newpath, titleSlug[p], p, '', '',)
                    grantAcces(art,group.id,1,1,1,0)
            else:
                grantAcces(article,groupT.id,1,1,0,0)
                for p in pagesToCreate[pages]:
                    art,npath = URLPath._create_urlpath_from_request_fromotherProject(
                        request, article, newpath, titleSlug[p], p, '', '',)
                    grantAcces(art,groupT.id,1,1,0,0)

        return redirect ('http://127.0.0.1:8000/logiciels/'+title)

# Création de la structure de Documentation pour un module de logiciel:
# Module
#   - Doc (doc user)
#      - Astuces
#   - T'Doc (doc technique)
#      - Installation et MAJ
#      - Debugs
#      - Astuces
class URLPathModuleViewSet(View):
    def get(self,request):

        logiciel =request.GET.get('logiciel').replace(' ','-').lower()
        title =request.GET.get('module')
        slug = title.lower().replace('&','').replace(' ','-')

        # création d'un groupe (qui comprendra acteurs GSI + ref métier)
        groupename = title.replace(' ','-').lower()
        groupenameT = groupename + '_tech'
        group = Group.objects.create(name=groupename)
        groupT = Group.objects.create(name=groupenameT)

        # Objets wiki nécessaires à la création des sous-pages logiciels
        ArticleLogiciel = Article.objects.get(id=5)
        URLPathLogiciel = URLPath.objects.get(slug = logiciel)
        # Création de la page Logiciel
        articleLog , newpathLog = URLPath._create_urlpath_from_request_fromotherProject(
            request, ArticleLogiciel, URLPathLogiciel, slug, title, '', '',)
        # Attributs pages à créer à la création d'un logiciel
        titleSlug ={}
        titleSlug["Doc"]="doc"
        titleSlug["Astuces"]="astuces"
        titleSlug["T'Doc"]="tdoc"
        titleSlug["Installation & MAJ"]="installation-maj"
        titleSlug["Debugs"]="debugs"
        pagesToCreate = {}
        pagesToCreate["Doc"] = ["Astuces"]
        pagesToCreate["T'Doc"] = ["Installation & MAJ","Debugs","Astuces"]
        # on envoie une requête à models.urlPaths.py:
        # - méthode _create_urlpath_from_request
        # - paramètres : cls, request, perm_article, parent_urlpath, slug, title, content, summary

        for pages in pagesToCreate:

            article,newpath = URLPath._create_urlpath_from_request_fromotherProject(
                request, articleLog, newpathLog, titleSlug[pages], pages, '', '',)
            if(pages == 'Doc'):
                grantAcces(article,group.id,1,1,1,0)
                for p in pagesToCreate[pages]:
                    art,npath = URLPath._create_urlpath_from_request_fromotherProject(
                        request, article, newpath, titleSlug[p], p, '', '',)
                    grantAcces(art,group.id,1,1,1,0)
            else:
                grantAcces(article,groupT.id,1,1,0,0)
                for p in pagesToCreate[pages]:
                    art,npath = URLPath._create_urlpath_from_request_fromotherProject(
                        request, article, newpath, titleSlug[p], p, '', '',)
                    grantAcces(art,groupT.id,1,1,0,0)

        return redirect ('http://127.0.0.1:8000/logiciels/'+title)


def grantAcces(article,groupId,groupread,groupwrite,otherread,otherwrite):
        Article.objects.filter(id= article.id).update(
        group_id = groupId,
        group_read = groupread,
        group_write = groupwrite,
        other_read = otherread,
        other_write = otherwrite,
)
