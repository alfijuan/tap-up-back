# TAP 2023 - Backend
Desarrollado por Juan Cruz Alfieri  
Materia TAP 2023 - Maria Belen Alegre

## Tecnologias
Se utilizo Python combinado con el framework web Django con una base de datos relacion SQLite3 que es portable y cumple el propisto para el ejercicio.


## Comandos
Django utiliza un set de comandos mediante el archivo `manage.py` 

- `python3 manage.py migrate` corre las migraciones y crea una db en caso de no tenerla
- `python3 manage.py cretesuperuser` crea un usuario disponible para la app. En caso de querer que sea admin, hay que cambiar el `type_id` del user creado haciendo
```
python3 manage.py shell      # para ingresar al shell de django

from django.contrib.auth.models import User   # importamos el modelo de User

u = User.objects.last()      # ultimo usuario recien creado
u.profile.type_id = '3003'   # codigo para administrador
u.save()                     # guarda el usuario
```

## Testing
Para el testing se utilizo el framework que provee django en conjunto con python y su herramienta de coverage

- `coverage run --source='.' manage.py test backend/tests/` correra los tests de la aplicacion y genera el reporte de coverage
- `coverage report` da el reporte producido por el comando anterior
