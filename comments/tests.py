from django.contrib.auth.models import User
from .models import Comment, Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTest(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian', password='pass2')
        self.post = Post.objects.create(title='Test post', content='Test content', owner=self.adam)

    def test_can_list_comments(self):
        # Create a comment
        Comment.objects.create(owner=self.brian, post=self.post, content='great!')

        # Test GET request for listing comments
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))
        