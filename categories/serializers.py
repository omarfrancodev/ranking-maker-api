from rest_framework import serializers
from .models import Category, Subcategory

class SubcategorySerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source='category.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category_id', 'category_name']

    def validate(self, data):
        if Subcategory.objects.filter(name=data['name'], category=data['category']).exists():
            raise serializers.ValidationError("A subcategory with this name already exists in the selected category.")
        return data

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
