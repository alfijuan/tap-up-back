from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from backend.models import Car, Appointment
import json

class AppointmentsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.car = Car.objects.create(
            owner=self.user, license='ABC123', year='2023', model='Ford'
        )
        self.appointment = Appointment.objects.create(
            vehicle=self.car, date='2023-11-20'
        )

    def test_create_appointment(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'vehicle': 'ABC123',
            'date': '2023-11-21'
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
            Appointment.objects.last().date.strftime('%Y-%m-%d'),
            data['date']
        )

    def test_list_appointments(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('api.appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appointment.vehicle.license)
        self.assertContains(response, self.appointment.date.strftime('%Y-%m-%d'))

    def test_list_appointments_unauthenticated(self):
        response = self.client.get(reverse('api.appointments'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'No hay usuario logueado'}
        )

    def test_delete_appointment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('api.appointments.item', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=self.appointment.id)
