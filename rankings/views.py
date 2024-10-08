from rest_framework import viewsets
from .models import RankingHeader
from .serializers import RankingHeaderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from utilities.mixins import CustomResponseMixin
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class RankingHeaderViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = RankingHeader.objects.all().prefetch_related(
        'ranking_items__content', 'person', 'category', 'subcategory')
    serializer_class = RankingHeaderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['person__id', 'category__id', 'subcategory__id']
    search_fields = ['person__name', 'category__name', 'subcategory__name']
    ordering_fields = ['person__name', 'category__name', 'subcategory__name']
    ordering = ['-person__name']

    @action(detail=False, methods=['get'])
    def by_person(self, request):
        person_id = request.query_params.get('person_id')
        if not person_id:
            raise ValidationError(
                {"detail": "El parámetro person_id es obligatorio."})

        rankings = RankingHeader.objects.filter(
            person__id=person_id).prefetch_related('ranking_items__content')
        serializer = self.get_serializer(rankings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category_subcategory(self, request):
        category_id = request.query_params.get('category_id')
        subcategory_id = request.query_params.get('subcategory_id')
        if not category_id or not subcategory_id:
            raise ValidationError(
                {"detail": "Los parámetros category_id y subcategory_id son obligatorios."})

        rankings = RankingHeader.objects.filter(
            category__id=category_id,
            subcategory__id=subcategory_id
        ).prefetch_related('ranking_items__content', 'person')
        serializer = self.get_serializer(rankings, many=True)
        return Response(serializer.data)
