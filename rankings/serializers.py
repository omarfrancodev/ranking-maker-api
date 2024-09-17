from rest_framework import serializers

from content.serializers import ContentListSerializer
from .models import RankingHeader, RankingItem
from users.models import Person
from categories.models import Category, Subcategory
from content.models import Content


class RankingItemSerializer(serializers.ModelSerializer):
    content = ContentListSerializer(read_only=True)
    content_id = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all())

    class Meta:
        model = RankingItem
        fields = ['id', 'content', 'content_id', 'rank']


class RankingHeaderSerializer(serializers.ModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all())
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all())
    ranking_items = serializers.ListSerializer(child=RankingItemSerializer())

    class Meta:
        model = RankingHeader
        fields = ['id', 'person_id', 'category_id',
                  'subcategory_id', 'ranking_items']

    def validate(self, data):
        person = data.get('person')
        category = data.get('category')
        subcategory = data.get('subcategory')

        print('person: ', person, 'category: ',
              category, 'subcategory: ', subcategory)

        valid_contents = Content.objects.filter(
            viewings__person=person,
            category=category,
            subcategories=subcategory
        ).distinct()
        print(valid_contents)

        for item in data.get('ranking_items', []):
            content = item.get('content')
            if content not in valid_contents:
                raise serializers.ValidationError({
                    'ranking_items': [{
                        'content': f"El contenido '{content}' no es válido para la categoría y subcategoría seleccionadas."
                    }]
                })

        return data

    def create(self, validated_data):
        ranking_items_data = validated_data.pop('ranking_items')

        ranking_header = RankingHeader.objects.create(
            person=validated_data['person'],
            category=validated_data['category'],
            subcategory=validated_data['subcategory'],
        )

        for item_data in ranking_items_data:
            item_data['ranking_header'] = ranking_header
            RankingItem.objects.create(**item_data)

        return ranking_header

    def update(self, instance, validated_data):
        items_data = validated_data.pop('ranking_items', None)

        instance.person = validated_data.get('person', instance.person)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get(
            'subcategory', instance.subcategory)
        instance.save()

        if items_data:
            instance.ranking_items.all().delete()

            valid_contents = Content.objects.filter(
                viewings__person=instance.person,
                category=instance.category,
                subcategories=instance.subcategory
            ).distinct()

            for item_data in items_data:
                content = item_data.get('content')
                if content not in valid_contents:
                    raise serializers.ValidationError({
                        'ranking_items': [{
                            'content': f"El contenido '{content}' no es válido para la categoría y subcategoría seleccionadas."
                        }]
                    })

                RankingItem.objects.create(
                    ranking_header=instance, **item_data)

        return instance
