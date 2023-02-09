from rest_framework import serializers

from .models import Product, UserProduct, Brand


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'brand',
            'name',
            'texture_ratings',
            'scent_ratings',
            'sentiment_ratings'
        ]


class UserProductSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = UserProduct
        fields = [
            'product',
            'custom_notes',
            'texture_notes',
            'texture_enjoyment',
            'scent_notes',
            'scent_enjoyment',
            'overall_sentiments'
        ]