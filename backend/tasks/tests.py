from django.test import TestCase

# Create your tests here.
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='john@mail.com', password='pass123')
        self.client.force_authenticate(user=self.user)
        self.list_url = '/api/tasks/tasks/'

    def test_create_task(self):
        data = {'title': 'My first task', 'description': 'This is a test'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My first task')

    def test_get_tasks_list(self):
        # Create sample task
        self.client.post(self.list_url, {'title': 'Task 1', 'description': 'Desc'})
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_update_task(self):
        task = self.client.post(self.list_url, {'title': 'Task 1'}).data
        update_url = f"{self.list_url}{task['id']}/"
        response = self.client.patch(update_url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated')

    def test_delete_task(self):
        task = self.client.post(self.list_url, {'title': 'Task to delete'}).data
        delete_url = f"{self.list_url}{task['id']}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
