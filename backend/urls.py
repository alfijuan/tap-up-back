from django.urls import path
from backend.views import users, cars, appointments

urlpatterns = [
  path('login/', users.api_login, name='api.login'),
  path('logout/', users.api_logout, name='api.logout'),
  path('me/', users.api_me, name='api.me'),

  path('cars/', cars.cars, name='api.cars'),
  path('cars/<id>/', cars.cars_item, name='api.cars.item'),

  path('appointments/', appointments.appointments, name='api.appointments'),
  path('appointments/<id>/', appointments.appointments_item, name='api.appointments.item'),
]