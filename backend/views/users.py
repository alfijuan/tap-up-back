from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from backend.helpers import get_request_body

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            post = get_request_body(request)
            if not post.get('username', None) or not post.get('password', None):
                return JsonResponse({'message': "El usuario y contraseña son requeridos"}, status=400)
            user = authenticate(request, username=post.get('username'), password=post.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'user': user.profile.to_json()}, status=200)
                return JsonResponse({'message': "El usuario no esta habilitado"}, status=400)
            return JsonResponse({'message': "Los datos ingresados no son válidos"}, status=400)
        else:
            return JsonResponse({'user': request.user.profile.to_json()}, status=200)
    return JsonResponse({'message': "Método no permitido", "code": "method_not_allowed"}, status=400)

@csrf_exempt
def api_me(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({'user': request.user.profile.to_json()}, status=200)
        else:
            return JsonResponse({'message': "No hay usuario logueado", 'code': 'no_logged_user'}, status=200)
    if request.method == 'PATCH':
        if request.user.is_authenticated:
            data = get_request_body(request)
            request.user.first_name = data.get("first_name")
            request.user.last_name = data.get("last_name")
            request.user.save()
            return JsonResponse({'user': request.user.profile.to_json()}, status=200)
    return JsonResponse({'message': "Método no permitido", "code": "method_not_allowed"}, status=400)

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': "Usuario deslogueado"})
        return JsonResponse({'message': "No hay usuario logueado", "code": "no_logged_user"}, status=400)
    return JsonResponse({'message': "Método no permitido", "code": "method_not_allowed"}, status=400)

@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            post = get_request_body(request)
            if not post.get('fullName', None) or not post.get('password', None) or not post.get('username', None) or not post.get('passwordB', None):
                return JsonResponse({'message': "El usuario, contraseña y nombre son requeridos"}, status=400)
            if post['password'] == post['passwordB']:
                try:
                    user = User.objects.get(username=post['username'])
                    return JsonResponse({'message': "El email ya esta asociado a una cuenta"}, status=400)
                except:
                    user = User.objects.create_user(post['username'], post['username'], post['password'])
                    user.profile.full_name = post.get('fullName')
                    user.email = post.get('username')
                    user.profile.type_id = '0000'
                    user.save()
                    login(request, user)
                    return JsonResponse({'user': user.profile.to_json()}, status=200)
            return JsonResponse({'message': "Las contraseñas no coinciden"}, status=400)
        return JsonResponse({'message': "Ya hay un usuario logueado"}, status=400)
    return JsonResponse({'message': "Método no permitido", "code": "method_not_allowed"}, status=400)