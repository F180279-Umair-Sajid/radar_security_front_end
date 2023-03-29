from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from users.views import user_login


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='password123',
        )

    def test_valid_login(self):
        response = self.client.post(self.url, {
            'username': 'testuser@example.com',
            'password': 'password123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_invalid_login(self):
        response = self.client.post(self.url, {
            'username': 'testuser@example.com',
            'password': 'wrongpassword',
        })
        self.assertContains(response, 'Invalid email address or password')
        form = response.context['form']
        self.assertIsInstance(form, user_login)
        self.assertTrue(form.has_error('__all__'))

    def test_invalid_form(self):
        response = self.client.post(self.url, {})
        self.assertContains(response, 'Please correct the errors below')
        form = response.context['form']
        self.assertIsInstance(form, user_login)
        self.assertTrue(form.has_error('username'))
        self.assertTrue(form.has_error('password'))

    def test_password_strength(self):
        response = self.client.post(self.url, {
            'username': 'testuser@example.com',
            'password': 'password',
        })
        self.assertContains(response, 'This password is too short.')
