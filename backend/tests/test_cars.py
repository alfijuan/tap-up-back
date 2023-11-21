from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from backend.models import Car
import json

class CarsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', password='test'
        )
        self.car = Car.objects.create(
            owner=self.user, license='ABC123', year='2023', model='Who'
        )

    def test_create_car(self):
        self.client.login(username='test', password='test')
        data = {
            'license': 'ABC124',
            'model': 'Ford',
            'year': '1995'
        }
        response = self.client.post(
            reverse('api.cars'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Car.objects.count(), 2)
        self.assertEqual(
            Car.objects.last().license,
            data['license']
        )
        self.assertEqual(
            Car.objects.last().model,
            data['model']
        )
        self.assertEqual(
            Car.objects.last().year,
            data['year']
        )

    def test_list_cars(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('api.cars'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.license)
        self.assertContains(response, self.car.year)

    def test_list_cars_unauthenticated(self):
        response = self.client.get(reverse('api.cars'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'No hay usuario logueado'}
        )
    
    def test_update_car(self):
        self.client.login(username='test', password='test')
        url = reverse('api.cars.item', args=[self.car.id])
        data = {
            'license': 'DEF456',
            'model': 'Updated Model',
            'year': '2023'
        }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['license'], 'DEF456')
        self.assertEqual(response.json()['model'], 'Updated Model')
        self.assertEqual(response.json()['year'], '2023')

    def test_get_car(self):
        self.client.login(username='test', password='test')
        url = reverse('api.cars.item', args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['license'], 'ABC123')
        self.assertEqual(response.json()['model'], 'Who')
        self.assertEqual(response.json()['year'], '2023')

    def test_delete_car(self):
        self.client.login(username='test', password='test')
        url = reverse('api.cars.item', args=[self.car.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Auto eliminado')
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())