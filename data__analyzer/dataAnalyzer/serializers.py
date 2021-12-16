from dataAnalyzer.models import Item
from rest_framework import serializers

from dataAnalyzer.models import Category


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'item_type', 'current_date', 'current_price', 'link']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']
