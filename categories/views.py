from rest_framework import viewsets
from .models import Category, Subcategory
from .serializers import CategorySerializer, SubcategorySerializer
from utilities.mixins import CustomResponseMixin

class CategoryViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
