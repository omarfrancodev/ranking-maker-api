from rest_framework import serializers
from content.models import Content
from users.models import Person
from .models import Viewing
from users.serializers import PersonSerializer
from content.serializers import ContentListSerializer


class ViewingSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all())

    class Meta:
        model = Viewing
        fields = ['id', 'person', 'content', 'date_viewed']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Viewing.objects.all(),
                fields=['person', 'content'],
                message="Esta persona ya ha visto este contenido."
            )
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = PersonSerializer(instance.person).data
        representation['content'] = ContentListSerializer(
            instance.content).data
        return representation
