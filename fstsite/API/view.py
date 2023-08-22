from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

import sql_test.models as sqlm
from .serializers import ArticleSerializer, ClientSerializer, ComponentSerializer


class ArticleViewset(ModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        querySet = sqlm.Article.objects.all()

        articleId = self.request.GET.get('id')
        if articleId is not None:
            querySet = querySet.filter(id=articleId)
        return querySet

class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        querySet = sqlm.Client.objects.all()

        clientId = self.request.GET.get('id')
        if clientId is not None:
            querySet = querySet.filter(id=clientId)
        return querySet

class ComponentViewset(ModelViewSet):

    serializer_class = ComponentSerializer

    def get_queryset(self):
        querySet = sqlm.Component.objects.all()

        componentId = self.request.GET.get('id')

        if componentId is not None:
            querySet = querySet.filter(id=componentId)
        return querySet