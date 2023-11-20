# modulos de rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'admin',
        'help',
        'token',
        'token/refresh',
        'chat',
        'chat/generar_prediccion',
        'chat/guardar',
        'chat/historial/<int:id_usuario>',
        'chat/historial/mensaje',
        'usuario',
        'usuario/<str:user_email>',
        'pdf/<int:id_prediccion>'
    ]
    return Response(routes)