# Backend HealthDiagAI

## Dependencias

Para instalar las dependencias necesarias, una vez clonado el repositorio, ejecute la siguiente instrucción en la consola:

```
pip install -r requirements.txt
```

## Arrancar el servidor

Para arrancar el servidor, una vez instaladas las dependencias, ejecute la siguiente instrucción en la consola:

```
python manage.py runserver
```

## Endpoints

- `/prediccion [POST]`: dada una ficha médica, devuelve la predicción de 5 posibles enfermedades y 5 especialistas.
