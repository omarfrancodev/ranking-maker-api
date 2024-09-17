from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer
from utilities.mixins import CustomResponseMixin

class PersonViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
