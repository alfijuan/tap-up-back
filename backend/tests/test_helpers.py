from django.test import TestCase
from django.contrib.auth.models import User
from backend.helpers import get_request_body, get_user
import json
from base64 import urlsafe_b64encode

class UtilsTestCase(TestCase):
    def test_get_request_body(self):
        request = type('Request', (object,), {
            'body': json.dumps({'asd': 'qwe'}).encode('utf-8')
        })
        self.assertEqual(get_request_body(request), {'asd': 'qwe'})

    def test_get_user(self):
        user = User.objects.create_user(
            username='test', password='test'
        )
        uidb64 = urlsafe_b64encode(str(user.pk).encode()).decode()
        self.assertEqual(get_user(uidb64), user)

    def test_get_user_invalid(self):
        self.assertIsNone(get_user('invalid_uidb64'))