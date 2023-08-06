from kuldeep.models import Harvest, Bread
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'