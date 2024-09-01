import uuid
from django.db import models
from categories.models import Category
from categories.models import Subcategory

class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='contents')
    subcategories = models.ManyToManyField(Subcategory, related_name='contents')

    def __str__(self):
        return self.name