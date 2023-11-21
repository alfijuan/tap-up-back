from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from backend.models import Car, Appointment
import json
from datetime import datetime


date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
class AppointmentsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', password='test'
        )
        self.car = Car.objects.create(
            owner=self.user, license='ABC123', year='2023', model='Ford'
        )
        self.appointment = Appointment.objects.create(
            vehicle=self.car, date=datetime.strptime('2023-11-20T03:00:00.000000Z', date_format)
        )

    def test_create_appointment(self):
        self.client.login(username='test', password='test')
        data = {
            'vehicle': 'ABC123',
            'date': '2023-11-20T03:00:00.000000Z'
        }
        response = self.client.post(
            reverse('api.appointments'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(
            Appointment.objects.last().vehicle.license,
            data['vehicle']
        )
        self.assertEqual(
            Appointment.objects.last().date.strftime(date_format),
            data['date']
        )
        self.assertEqual(
            Appointment.objects.last().score,
            ''
        )

    def test_list_appointments(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('api.appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appointment.vehicle.license)
        self.assertContains(response, self.appointment.date.strftime(date_format))

    def test_list_appointments_unauthenticated(self):
        response = self.client.get(reverse('api.appointments'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'No hay usuario logueado'}
        )

    def test_update_appointment(self):
        self.client.login(username='test', password='test')
        data = {
            'vehicle': 'ABC123',
            'date': '2023-11-20T03:00:00.000000Z'
        }
        response = self.client.patch(
            reverse('api.appointments.item', args=[self.appointment.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.vehicle.license, data['vehicle'])
        self.assertEqual(self.appointment.date.strftime(date_format), data['date'])

    def test_get_appointment(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('api.appointments.item', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appointment.vehicle.license)
        self.assertContains(response, self.appointment.date.strftime(date_format))

    def test_delete_appointment(self):
        self.client.login(username='test', password='test')
        response = self.client.delete(reverse('api.appointments.item', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=self.appointment.id)
