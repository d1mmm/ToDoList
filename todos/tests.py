from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import TodoItem
from django.utils import timezone
from datetime import timedelta


class TodoItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email='testuser@test.com', password='password')
        self.client.login(username='testuser', password='password')

        response = self.client.post(reverse('rest_login'), data={
            'email': 'testuser@test.com',
            'password': 'password'
        })
        self.token = response.data.get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_todo_item(self):
        url = reverse('todoitem-list')
        data = {
            'title': 'Test Todo',
            'description': 'Test Description',
            'completed': False,
            'due_date': (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_todo_item_with_past_due_date(self):
        url = reverse('todoitem-list')
        data = {
            'title': 'Test Todo',
            'description': 'Test Description',
            'completed': False,
            'due_date': (timezone.now()).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_todo_items(self):
        TodoItem.objects.create(user=self.user, title='Test Todo', due_date=timezone.now() + timedelta(days=1))
        url = reverse('todoitem-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_filter_todo_items_by_completed(self):
        TodoItem.objects.create(user=self.user, title='Completed Todo', completed=True, due_date=timezone.now() + timedelta(days=1))
        TodoItem.objects.create(user=self.user, title='Incomplete Todo', completed=False, due_date=timezone.now() + timedelta(days=1))
        url = reverse('todoitem-list')
        response = self.client.get(url + '?completed=True', format='json')
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)

    def test_filter_todo_items_by_due_date(self):
        TodoItem.objects.create(user=self.user, title='Todo 1', due_date=timezone.now() + timedelta(days=1))
        TodoItem.objects.create(user=self.user, title='Todo 2', due_date=timezone.now() + timedelta(days=3))
        url = reverse('todoitem-list')
        response = self.client.get(url + '?due_date_after=' + (timezone.now() + timedelta(days=2)).isoformat(), format='json')
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)

    def test_update_todo_item(self):
        todo = TodoItem.objects.create(user=self.user, title='Test Todo', due_date=timezone.now() + timedelta(days=1))
        url = reverse('todoitem-detail', args=[todo.id])
        data = {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'completed': True,
            'due_date': (timezone.now() + timedelta(days=2)).isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_todo_item(self):
        todo = TodoItem.objects.create(user=self.user, title='Test Todo', due_date=timezone.now() + timedelta(days=1))
        url = reverse('todoitem-detail', args=[todo.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
