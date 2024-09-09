from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Viewing
from .serializers import ViewingSerializer
from utilities.mixins import CustomResponseMixin


class ViewingViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Viewing.objects.all()
    serializer_class = ViewingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['person__id', 'content__id', 'date_viewed']
    search_fields = ['person__name', 'content__name']
    ordering_fields = ['date_viewed']
    ordering = ['-date_viewed']
