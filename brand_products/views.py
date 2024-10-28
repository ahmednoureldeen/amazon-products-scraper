from requests import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['brand']
    search_fields =  ['name', 'asin', 'sku']
