from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)

    def clean(self):
        if self.due_date and self.due_date <= timezone.now():
            raise ValidationError('Due date must be in the future.')

    def save(self, *args, **kwargs):
        self.clean()
        super(TodoItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
