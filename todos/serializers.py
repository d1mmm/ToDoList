from rest_framework import serializers
from .models import TodoItem
from django.utils import timezone


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'description', 'completed', 'due_date', 'user']
        read_only_fields = ['user']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Due date must be in the future.')
        return value
