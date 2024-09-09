from rest_framework import serializers
from .models import Content
from categories.serializers import CategorySerializer, SubcategoryReadOnlySerializer
from categories.models import Category, Subcategory
from viewings.models import Viewing
from users.serializers import PersonSerializer
from users.models import Person


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    subcategories = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(),
        many=True
    )

    class Meta:
        model = Content
        fields = ['id', 'name', 'category', 'subcategories']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        category = attrs.get('category', getattr(instance, 'category', None))
        subcategories = attrs.get('subcategories', getattr(
            instance, 'subcategories', None))

        if category and subcategories:
            invalid_subcategories = [
                sub for sub in subcategories if sub.category != category]
            if invalid_subcategories:
                raise serializers.ValidationError({
                    'subcategories': f"Las siguientes subcategorías no pertenecen a la categoría seleccionada: {', '.join(str(sub) for sub in invalid_subcategories)}"
                })

        return attrs

    def create(self, validated_data):
        subcategories = validated_data.pop('subcategories', [])
        content = Content.objects.create(**validated_data)
        content.subcategories.set(subcategories)
        return content

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            instance.category = validated_data['category']
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'subcategories' in validated_data:
            instance.subcategories.set(validated_data['subcategories'])
        instance.save()
        return instance


class ContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'name']


class ContentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategories = SubcategoryReadOnlySerializer(many=True)

    class Meta:
        model = Content
        fields = ['id', 'name', 'category', 'subcategories']


class ViewingDetailSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Viewing
        fields = ['person', 'date_viewed']


class ContentWithViewingsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategories = SubcategoryReadOnlySerializer(many=True)
    viewing = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'name', 'category',
                  'subcategories', 'viewing', 'views']

    def get_viewing(self, obj):
        viewings = Viewing.objects.filter(content=obj)
        return ViewingDetailSerializer(viewings, many=True).data

    def get_views(self, obj):
        return Viewing.objects.filter(content=obj).count()


class ContentFilterSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategories = SubcategoryReadOnlySerializer(many=True)
    persons = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'name', 'category', 'subcategories', 'persons']

    def get_persons(self, obj):
        viewings = Viewing.objects.filter(content=obj)
        return [
            {
                'person_id': viewing.person.id,
                'name': viewing.person.name,
                'date_viewed': viewing.date_viewed
            }
            for viewing in viewings
        ]
