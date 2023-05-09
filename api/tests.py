from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Blogs

import json

class EndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword') 
        self.blog = Blogs.objects.create(title='Test Blog', content='This is a test blog.', author=self.user)
        self.login_user()




    def test_register_user(self):
        url = reverse('api:register')
        data = {'username': 'newuser','email':'new@test.com', 'password': 'newpassword'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)




    def login_user(self):
        url = reverse('api:login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        response_data = response.json()
        print(response_data)
        token = response_data['token']

        # Store the token for later use
        self.token = token



    def test_create_blog(self):
        headers = {'Authorization': f'Token {self.token}'}
        url = reverse('api:create-blog')
        data = {'title': 'New Blog', 'content': 'This is a new blog.'}
        print(data)
        response = self.client.post(url, data=data, headers=headers)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blogs.objects.count(), 2)

        




    def test_list_all_blogs(self):
        url = reverse('api:list-all-blogs')
        response = self.client.get(url, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['Blogs']), 1)




    def test_list_one_blog(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:list-one-blog', kwargs={'pk': self.blog.id})
        response = self.client.get(url, headers={'Authorization': f'Token {self.token}'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Blog']['title'], self.blog.title)



    def test_edit_blog(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:edit-blog', kwargs={'pk': self.blog.id})
        data = {'title': 'Updated Blog', 'content': 'This is an updated blog.'}
        response = self.client.put(url, data=data, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Blogs.objects.get(id=self.blog.id).title, 'Updated Blog')




    def test_delete_blog(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:delete-blog', kwargs={'pk': self.blog.id})
        response = self.client.delete(url, headers={'Authorization': f'Token {self.token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Blogs.objects.count(), 0)