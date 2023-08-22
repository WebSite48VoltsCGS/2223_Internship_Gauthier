from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

import sql_test.models as sqlm
from .serializers import ArticleSerializer, ClientSerializer, ComponentSerializer,\
                         CommandSerializer, CommandLineSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class ArticleViewset(ModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        querySet = sqlm.Article.objects.all()

        articleId = self.request.GET.get('id')
        if articleId is not None:
            querySet = querySet.filter(id=articleId)
        return querySet

class AdminArticleViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return sqlm.Article.objects.all()

class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        querySet = sqlm.Client.objects.all()

        clientId = self.request.GET.get('id')
        if clientId is not None:
            querySet = querySet.filter(id=clientId)
        return querySet

class AdminClientViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ClientSerializer

    def get_queryset(self):
        return sqlm.Client.objects.all()

class ComponentViewset(ModelViewSet):

    serializer_class = ComponentSerializer

    def get_queryset(self):
        querySet = sqlm.Component.objects.all()

        componentId = self.request.GET.get('id')

        if componentId is not None:
            querySet = querySet.filter(id=componentId)
        return querySet

class AdminComponentViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ComponentSerializer

    def get_queryset(self):
        return sqlm.Component.objects.all()

class CommandViewset(ModelViewSet):

    serializer_class = CommandSerializer

    def get_queryset(self):
        querySet = sqlm.Command.objects.all()

        commandId = self.request.GET.get('id')

        if commandId is not None:
            querySet = querySet.filter(id=commandId)
        return querySet

class AdminCommandViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommandSerializer

    def get_queryset(self):
        return sqlm.Command.objects.all()

class CommandLineViewset(ModelViewSet):

    serializer_class = CommandLineSerializer

    def get_queryset(self):
        querySet = sqlm.CommandLine.objects.all()

        commandLineId = self.request.GET.get('id')

        if commandLineId is not None:
            querySet = querySet.filter(id=commandLineId)
        return querySet

class AdminCommandLineViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommandLineSerializer

    def get_queryset(self):
        return sqlm.CommandLine.objects.all()