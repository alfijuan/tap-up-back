from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from backend.models import Car
from backend.helpers import get_request_body

@csrf_exempt
def cars(request):
    if request.user.is_authenticated:
        # Crea un auto
        if request.method == 'POST':
            post = get_request_body(request)
            if not post.get('license', None):
                return JsonResponse({'message': "La patente es requerida"}, status=400)
            try:
                get_object_or_404(Car, id=post.get('license'))
                return JsonResponse({'message': "El auto ya existe"}, status=400)
            except: 
                newCar = Car(
                    license=post.get('license'),
                    model=post.get('model'),
                    year=post.get('year'),
                    owner=request.user
				)
                newCar.save()
                return JsonResponse(newCar.to_json(), status=200)
        
        # List cars
        if request.method == 'GET':
            if request.user.profile.type_id != '3003':
                objects = request.user.cars.all()
            else:
                # Is admin
                objects = Car.objects.all()
            return JsonResponse({"cars": [x.to_json() for x in objects]}, status=200)
        return JsonResponse({'message': "Método no permitido"}, status=400)
    return JsonResponse({'message': "No hay usuario logueado"}, status=400)


@csrf_exempt
def cars_item(request, id):
    if request.user.is_authenticated:
        # Crea un auto
        if request.user.profile.type_id != '3003':
            objects = Car.objects.filter(owner=request.user)
        else:
            objects = Car.objects.all()
        item = get_object_or_404(objects, id=id)
        
        if request.method == 'PATCH':
            post = get_request_body(request)
            if not post.get('license', None):
                return JsonResponse({'message': "La patente es requerida"}, status=400)
            item.license = post.get('license')
            item.model = post.get('model')
            item.year = post.get('year')
            item.save()
            return JsonResponse(item.to_json(), status=200)
        
        # get Car
        if request.method == 'GET':
            return JsonResponse(item.to_json(), status=200)
        if request.method == 'DELETE':
            item.delete()
            return JsonResponse({'message': "Auto eliminado"}, status=200)
        return JsonResponse({'message': "Método no permitido"}, status=400)
    return JsonResponse({'message': "No hay usuario logueado"}, status=400)
        