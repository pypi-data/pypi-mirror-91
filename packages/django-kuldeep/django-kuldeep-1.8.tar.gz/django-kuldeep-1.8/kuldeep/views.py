from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import exceptions
from kuldeep.models import Harvest, Bread
from kuldeep.serializers import HarvestSerializer, BreadSerializer

# Create your views here.
class HarvestViewSet(viewsets.ModelViewSet):
    """
    Perform CRUD operations in Harvest.
    """
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer


class BreadViewSet(viewsets.ModelViewSet):
    """
    Perform CRUD operations in Bread.
    """
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer