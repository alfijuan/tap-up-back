from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json

class ApiLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', password='test'
        )

    def test_login_success(self):
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(
            reverse('api.login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.profile.to_json()['username'])

    def test_login_failure(self):
        data = {
            'username': 'test',
            'password': 'wrongpass'
        }
        response = self.client.post(
            reverse('api.login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Los datos ingresados no son válidos'}
        )

    def test_login_unauthenticated(self):
        response = self.client.get(reverse('api.login'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Método no permitido', 'code': 'method_not_allowed'}
        )

    def test_me_success(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('api.me'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.profile.to_json()['username'])

    def test_me_patch_success(self):
        self.client.login(username='test', password='test')
        newData = {
            'first_name': 'Juan'
        }
        response = self.client.patch(
            reverse('api.me'),
            json.dumps(newData),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.profile.to_json()['first_name'])

    def test_logout_success(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('api.logout'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': "Usuario deslogueado"}
        )

    def test_logout_unauthenticated(self):
        response = self.client.post(
            reverse('api.logout'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': "No hay usuario logueado", "code": "no_logged_user"}
        )

