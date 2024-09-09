from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Content
from utilities.mixins import CustomResponseMixin
from .serializers import (
    ContentCreateUpdateSerializer,
    ContentListSerializer,
    ContentDetailSerializer,
    ContentWithViewingsSerializer,
    ContentFilterSerializer
)


class ContentViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Content.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category__id', 'subcategories__id']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentListSerializer
        elif self.action == 'retrieve':
            return ContentDetailSerializer
        elif self.action == 'list_with_viewings':
            return ContentWithViewingsSerializer
        elif self.action == 'filter_contents':
            return ContentFilterSerializer
        else:
            return ContentCreateUpdateSerializer

    @action(detail=False, methods=['get'], url_path='with-viewings')
    def list_with_viewings(self, request):
        contents = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(contents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(contents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='filter')
    def filter_contents(self, request):
        category_id = request.query_params.get('category')
        subcategory_id = request.query_params.get('subcategory')
        person_id = request.query_params.get('person')

        queryset = self.get_queryset()

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategories__id=subcategory_id)
        if person_id:
            queryset = queryset.filter(viewings__person__id=person_id)

        queryset = queryset.distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
