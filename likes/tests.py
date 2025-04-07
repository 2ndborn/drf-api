from django.contrib.auth.models import User
from .models import Like, Post
from rest_framework import status
from rest_framework.test import APITestCase


class LikeListViewTest(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian', password='pass2')
        self.post = Post.objects.create(title='test title', content='test content', owner=self.adam)

    def test_can_list_likes(self):
        Like.objects.create(post=self.post, owner=self.brian)
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(response.data[0]['owner'], self.brian.username)
        print(response.data)
        print(len(response.data))

