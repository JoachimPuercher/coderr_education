from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class RegistrationTests(APITestCase):

    def setUp(self):
        self.url = reverse('registration')
        self.data = {
            'username': 'testuser',
            'email': 'test@mail.de',
            'password': 'SicheresPW123',
            'repeated_password': 'SicheresPW123',
            'type': 'customer',
        }

    def test_registration_creates_user(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@mail.de')

    def test_registration_returns_token_and_user_data(self):
        response = self.client.post(self.url, self.data, format='json')
        user = User.objects.get(username='testuser')

        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@mail.de')
        self.assertEqual(response.data['user_id'], user.pk)
        self.assertEqual(response.data['token'], Token.objects.get(user=user).key)

    def test_registration_creates_profile_with_type(self):
        self.client.post(self.url, self.data, format='json')

        profile = UserProfile.objects.get(user__username='testuser')
        self.assertEqual(profile.type, 'customer')

    def test_password_is_hashed_and_not_returned(self):
        response = self.client.post(self.url, self.data, format='json')
        user = User.objects.get(username='testuser')

        self.assertNotEqual(user.password, self.data['password'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertNotIn('password', response.data)

    def test_passwords_do_not_match(self):
        data = {**self.data, 'repeated_password': 'AnderesPW123'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_username_already_taken(self):
        User.objects.create_user(username='testuser', password='irgendwas')
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_email_already_taken(self):
        User.objects.create_user(username='andereruser', email='test@mail.de', password='irgendwas')
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_email_comparison_ignores_case(self):
        User.objects.create_user(username='andereruser', email='test@mail.de', password='irgendwas')
        data = {**self.data, 'email': 'TEST@MAIL.DE'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_user_type(self):
        data = {**self.data, 'type': 'admin'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
