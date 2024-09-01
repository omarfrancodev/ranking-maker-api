import uuid
from django.db import models
from users.models import Person
from content.models import Content
from categories.models import Category
from categories.models import Subcategory

class RankingHeader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='ranking_headers')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ranking_headers')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='ranking_headers')

    class Meta:
        unique_together = ('person', 'category', 'subcategory')

    def __str__(self):
        return f"{self.person.name} - {self.category.name} - {self.subcategory.name}"

class RankingItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranking_header = models.ForeignKey(RankingHeader, on_delete=models.CASCADE, related_name='ranking_items')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='ranking_items')
    rank = models.PositiveIntegerField()

    class Meta:
        unique_together = ('ranking_header', 'content', 'rank')

    def __str__(self):
        return f"{self.content.name} - Rank: {self.rank}"