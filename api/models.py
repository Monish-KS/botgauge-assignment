from django.db import models
from django.utils import timezone

class Item(models.Model):
    key = models.CharField(max_length=255, unique=True, db_index=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.key}: {self.value}"
