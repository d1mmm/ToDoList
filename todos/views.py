from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from .models import TodoItem
from .serializers import TodoItemSerializer


class TodoItemFilter(filters.FilterSet):
    due_date = filters.DateFromToRangeFilter()
    completed = filters.BooleanFilter()

    class Meta:
        model = TodoItem
        fields = ['due_date', 'completed']


class TodoItemViewSet(viewsets.ModelViewSet):
    serializer_class = TodoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TodoItemFilter

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
