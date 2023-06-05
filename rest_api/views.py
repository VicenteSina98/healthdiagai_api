from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .functions import *


class PrediccionListAPIView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        ficha_medica = generar_ficha_medica(request.data)
        prediccion = generar_prediccion(ficha_medica)
        # error en la generacion del prediccion
        if 'errorCode' in prediccion.keys():
            return Response(prediccion, status=prediccion['errorStatus'])
        # prediccion OK
        prediccion_list = prediccion['prediccion'].split('\n')
        posibles_enfermedades = prediccion_list[1:6]
        posibles_profesionales = prediccion_list[8:]
        data = {'posibles_enfermedades': posibles_enfermedades,
                'posibles_profesionales': posibles_profesionales}
        return Response(data, status=status.HTTP_200_OK)
