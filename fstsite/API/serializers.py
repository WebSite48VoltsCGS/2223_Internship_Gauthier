from rest_framework.serializers import ModelSerializer

import sql_test.models as sqlm


class ComponentSerializer(ModelSerializer):

    class Meta:
        model = sqlm.Component
        fields = ['kit',
                  'article',
                  'number']

class ArticleSerializer(ModelSerializer):

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

class ClientSerializer(ModelSerializer):

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
