from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from backend.models import Car, Appointment
from backend.helpers import get_request_body
from datetime import datetime

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

@csrf_exempt
def appointments(request):
    if request.user.is_authenticated:
        # Crea un appointment
        if request.method == 'POST':
            post = get_request_body(request)
            if not post.get('vehicle', None):
                return JsonResponse({'message': "La patente es requerida"}, status=400)
            car = get_object_or_404(Car, license=post.get('vehicle'))
            newItem = Appointment(
                vehicle=car,
                date=datetime.strptime(post.get('date'), date_format)
			)
            newItem.save()
            return JsonResponse(newItem.to_json(), status=200)
        
        # List appointments
        if request.method == 'GET':
            if request.user.profile.type_id != '3003':
                cars = request.user.cars.all()
                objects = Car.objects.none()
                for x in cars:
                    objects = objects | x.appointments.all()
            else:
                # Is admin
                objects = Appointment.objects.all()
            return JsonResponse({"appointments": [x.to_json() for x in objects]}, status=200)
        return JsonResponse({'message': "Método no permitido"}, status=400)
    return JsonResponse({'message': "No hay usuario logueado"}, status=400)

@csrf_exempt
def appointments_item(request, id):
    if request.user.is_authenticated:
        if request.user.profile.type_id != '3003':
            cars = request.user.cars.all()
            objects = Car.objects.none()
            for x in cars:
                objects = objects | x.appointments.all()
        else:
            objects = Appointment.objects.all()
        item = get_object_or_404(objects, id=id)
        
        if request.method == 'PATCH':
            post = get_request_body(request)

            if post.get('vehicle'):
                item.vehicle = get_object_or_404(Car, license=post.get('vehicle'))
            item.date = datetime.strptime(post.get('date'), date_format)

            if request.user.profile.type_id == '3003':
                item.score = post.get('score')
                item.comments = post.get('comments', '')
            
            item.save()
            return JsonResponse(item.to_json(), status=200)
        
        # get Car
        if request.method == 'GET':
            return JsonResponse(item.to_json(), status=200)
        if request.method == 'DELETE':
            item.delete()
            return JsonResponse({'message': "Reserva eliminada"}, status=200)
        return JsonResponse({'message': "Método no permitido"}, status=400)
    return JsonResponse({'message': "No hay usuario logueado"}, status=400)