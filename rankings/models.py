import uuid
from django.db import models
from users.models import Person
from content.models import Content
from categories.models import Category
from categories.models import Subcategory

class Ranking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='rankings')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='rankings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rankings')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='rankings')
    rank = models.PositiveIntegerField()

    class Meta:
        unique_together = ('person', 'category', 'subcategory', 'rank')