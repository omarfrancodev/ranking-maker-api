from rest_framework import viewsets
from .models import Viewing
from .serializers import ViewingSerializer
from rest_framework.decorators import action
from utilities.mixins import CustomResponseMixin
from rest_framework.exceptions import ValidationError, NotFound


class ViewingViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Viewing.objects.all()
    serializer_class = ViewingSerializer

    @action(detail=False, methods=['get'])
    def by_content(self, request):
        content_id = request.query_params.get('content_id')
        if not content_id:
            raise ValidationError(
                {"detail": "content_id parameter is required."})

        viewings = Viewing.objects.filter(
            content__id=content_id).select_related('person')
        if not viewings.exists():
            raise NotFound(
                {"detail": "No viewings found for the given content."})

        data = [
            {
                "person": viewing.person.name,
                "date_viewed": viewing.date_viewed
            }
            for viewing in viewings
        ]
        return self.create_response(request, data, "Viewings by content retrieved successfully.")

    @action(detail=False, methods=['get'])
    def by_person(self, request):
        person_id = request.query_params.get('person_id')
        if not person_id:
            raise ValidationError(
                {"detail": "person_id parameter is required."})

        viewings = Viewing.objects.filter(
            person__id=person_id).select_related('content')
        if not viewings.exists():
            raise NotFound(
                {"detail": "No viewings found for the given person."})

        data = [
            {
                "content": viewing.content.name,
                "date_viewed": viewing.date_viewed
            }
            for viewing in viewings
        ]
        return self.create_response(request, data, "Viewings by person retrieved successfully.")
