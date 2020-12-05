from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
