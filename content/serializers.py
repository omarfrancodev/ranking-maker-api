from rest_framework import serializers
from .models import Content
from categories.models import Category, Subcategory

class ContentSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategories = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all(), many=True)

    class Meta:
        model = Content
        fields = ['id', 'name', 'category', 'subcategories']

    def validate(self, data):
        category = data.get('category')
        subcategories = data.get('subcategories', [])

        # Ensure subcategories belong to the given category
        for subcategory in subcategories:
            if subcategory.category != category:
                raise serializers.ValidationError({
                    'subcategories': f'Subcategory {subcategory.name} does not belong to the selected category.'
                })

        return data

    def create(self, validated_data):
        category = validated_data.pop('category')
        subcategories = validated_data.pop('subcategories')

        content = Content.objects.create(category=category, **validated_data)

        # Set valid subcategories that belong to the selected category
        content.subcategories.set(subcategories)

        return content

    def update(self, instance, validated_data):
        category = validated_data.pop('category', None)
        subcategories = validated_data.pop('subcategories', None)

        if category:
            instance.category = category

        if subcategories is not None:
            # Set valid subcategories that belong to the selected category
            instance.subcategories.set(subcategories)

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
