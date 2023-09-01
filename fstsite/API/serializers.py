from rest_framework import serializers
from rest_framework.response import Response

import sql_test.models as sqlm


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = sqlm.Component
        fields = ['kit',
                  'article',
                  'number']

    def validate(self, data):
        try:
            if len(sqlm.Component.objects.filter(article=data['article'], kit=data['kit'])) > 1:
                raise serializers.ValidationError("Cannot have the same item twice in the same pack.")
            return data
        except _:
            return data

class ArticleSerializer(serializers.ModelSerializer):

    article = serializers.SerializerMethodField()

    class Meta:
        model = sqlm.Article
        fields = ['internal_id',
                  'product',
                  'brand',
                  'category',
                  'sub_category',
                  'denomination',
                  'description',
                  'sell_or_loc',
                  'is_multiple',
                  'article',
                  'buying_price',
                  'stock',
                  'location_price',
                  'weight',
                  'minimal_lot', ]

    def get_article(self, instance):

        queryset = sqlm.Component.objects.filter(kit=instance.id)
        serializer = ComponentSerializer(queryset, many=True)
        return serializer.data




class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = sqlm.Client
        fields = ['asso',
                  'siret',
                  'adress',
                  'name',
                  'user_name',
                  'user_lastname',
                  'email',
                  'phone', ]

class CommandSerializer(serializers.ModelSerializer):

    billing_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    paiment_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    start_loc = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    end_loc = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    articles = serializers.SerializerMethodField()

    class Meta:
        model = sqlm.Command
        fields = ['billing_id',
                  'client',
                  'description',
                  'articles',
                  'is_payed',
                  'billing_date',
                  'paiment_date',
                  'loc_place',
                  'deposit',
                  'start_loc',
                  'end_loc', ]

    def get_articles(self, instance):

        queryset = sqlm.CommandLine.objects.filter(command=instance.id)
        serializer = CommandLineSerializer(queryset, many=True)
        return serializer.data

class CommandLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = sqlm.CommandLine
        fields = ['command',
                  'article',
                  'number',
                  'coeff',
                  'discount', ]

    def validate(self, data):
        if sqlm.CommandLine.objects.filter(article=data['article'], command=data['command']).exists():
            raise serializers.ValidationError("Cannot have the same item twice in the same bid.")
        return data