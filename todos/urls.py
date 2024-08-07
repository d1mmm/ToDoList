from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoItemViewSet

router = DefaultRouter()
router.register(r'todos', TodoItemViewSet, basename='todoitem')

urlpatterns = [
    path('', include(router.urls)),
]
