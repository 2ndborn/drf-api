from django.contrib.auth.models import User
from .models import Comment, Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTest(APITestCase):
    def setUp(self):
        # Create users and posts
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

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='brian', password='pass2')
        comment_data = {'post': self.post.id, 'content': 'test content'}
        response = self.client.post('/comments/', comment_data)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_comment(self):
        comment_data = {'post': self.post.id, 'content': 'test content'}
        response = self.client.post('/comments/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CommentDetailViewTest(APITestCase):
    def setUp(self):
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian', password='pass')
        self.post = Post.objects.create(
            owner=self.adam, title='a title', content='adams content'
        )
        self.post2 = Post.objects.create(
            owner=self.brian, title='a title', content='brians content'
        )
        self.comment1 = Comment.objects.create(
            owner=self.adam, post=self.post, content='test content'
        )
        self.comment2 = Comment.objects.create(
            owner=self.adam, post=self.post, content='test content'
        )

    def test_can_retrieve_a_comment_using_valid_id(self):
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['content'], 'test content')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
