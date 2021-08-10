from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from wiki.models.urlpath import URLPath

from django.core.exceptions import ObjectDoesNotExist



class URLPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLPath
        fields = ['objects','owner']
         # ,'current_revision','created' ,'modified' ,'owner' ,'group','group_read','group_write','other_read','other_write']
