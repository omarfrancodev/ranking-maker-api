from rest_framework import serializers
from .models import Viewing
from users.models import Person
from content.models import Content

class ViewingSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    content = serializers.PrimaryKeyRelatedField(queryset=Content.objects.all())
    date_viewed = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = Viewing
        fields = ['id', 'person', 'content', 'date_viewed']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Viewing.objects.all(),
                fields=['person', 'content', 'date_viewed'],
                message="This viewing record already exists."
            )
        ]