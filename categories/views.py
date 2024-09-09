from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Category, Subcategory
from .serializers import CategoryDetailSerializer, CategorySerializer, SubcategorySerializer
from utilities.mixins import CustomResponseMixin
from rest_framework.decorators import action


class CategoryViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['list_with_subcategories', 'with_subcategories']:
            return CategoryDetailSerializer
        return CategorySerializer

    @action(detail=False, methods=['get'])
    def list_with_subcategories(self, request):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return self.create_response(request, serializer.data, "Categorías listadas con subcategorías correctamente")

    @action(detail=True, methods=['get'])
    def with_subcategories(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.get_serializer(category)
        return self.create_response(request, serializer.data, "Obtener categoría con subcategorías correctamente")


class SubcategoryViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
