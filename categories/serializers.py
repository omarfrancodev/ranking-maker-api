from rest_framework import serializers
from .models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subcategory.objects.all(),
                fields=['name', 'category'],
                message="Ya existe una subcategoría con este nombre en la categoría seleccionada."
            )
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['category'] = {
            'category_id': instance.category.id,
            'name': instance.category.name
        }
        return representation


class SubcategoryReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

    def get_subcategories(self, obj):
        return [
            {'subcategory_id': str(sub.id), 'name': sub.name}
            for sub in obj.subcategories.all()
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
