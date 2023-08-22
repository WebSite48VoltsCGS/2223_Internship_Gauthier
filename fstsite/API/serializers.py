from rest_framework import serializers

import sql_test.models as sqlm


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = sqlm.Component
        fields = ['kit',
                  'article',
                  'number']

    def validate(self, data):
        if sqlm.Component.objects.filter(article=data['article'], kit=data['kit']).exists():
            raise serializers.ValidationError("Cannot have the same item twice in the same pack.")
        return data

class ArticleSerializer(serializers.ModelSerializer):

    #article = serializers.SerializerMethodField()

    class Meta:
        model = sqlm.Article
        fields = ['product',
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

    class Meta:
        model = sqlm.Command
        fields = ['billing_id',
                  'client',
                  'articles',
                  'is_payed',
                  'billing_date',
                  'paiment_date',
                  'loc_place',
                  'start_loc',
                  'end_loc', ]

class CommandLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = sqlm.CommandLine
        fields = ['command',
                  'article',
                  'number']

    def validate(self, data):
        if sqlm.CommandLine.objects.filter(article=data['article'], kit=data['kit']).exists():
            raise serializers.ValidationError("Cannot have the same item twice in the same pack.")
        return data