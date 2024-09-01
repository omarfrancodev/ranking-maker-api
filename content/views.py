from rest_framework import viewsets
from .models import Content
from .serializers import ContentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Prefetch
from utilities.mixins import CustomResponseMixin

class ContentViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=False, methods=['get'])
    def with_view_counts(self, request):
        queryset = Content.objects.annotate(view_count=Count('viewings'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)