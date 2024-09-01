import uuid
from django.db import models
from users.models import Person
from content.models import Content

class Viewing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='viewings')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='viewings')
    date_viewed = models.DateField()

    class Meta:
        unique_together = ('person', 'content', 'date_viewed')
