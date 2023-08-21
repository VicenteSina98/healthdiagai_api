from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .functions import *
from .serializers import UsuarioSerializer, AntecedentesMedicosSerializer, MyTokenObtainPairSerializer, PrediccionSerializer, MensajeSerializer
from .models import Usuario, AntecedentesMedicos, Prediccion, Mensaje
import pprint


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token',
        'token/refresh',
        'register',
        'usuario/',
        'usuario/<str:user_email>',
        'prediccion/',
        'prediccion/generar',
        'prediccion/guardar',
        'prediccion/<int:id_usuario>',
    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        informacion_personal = data['informacionPersonal']
        antecedentes_medicos = data['antecedentesMedicos']
        user = User(username=informacion_personal['email'])
        user.set_password(informacion_personal['password'])
        user.save()
        usuario_serializer = UsuarioSerializer(data={
            'email': informacion_personal['email'],
            'nombres': informacion_personal['nombres'],
            'primer_apellido': informacion_personal['primerApellido'],
            'segundo_apellido': informacion_personal['segundoApellido'],
            'fecha_nacimiento': informacion_personal['fechaNacimiento'],
            'sexo': informacion_personal['sexo'],
            'altura': informacion_personal['altura'],
            'peso': informacion_personal['peso'],
            'user': user.pk
        })
        if not usuario_serializer.is_valid():
            print(usuario_serializer.errors)
            return Response(usuario_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        usuario_serializer.save()
        ant_medicos_serializer = AntecedentesMedicosSerializer(data={
            'usuario': Usuario.objects.get(email=usuario_serializer.data['email']).pk,
            'enfermedades_cronicas': antecedentes_medicos['enfermedadesCronicas'],
            'historial_alergias': antecedentes_medicos['historialAlergias'],
            'historial_cirugias': antecedentes_medicos['historialCirugias'],
            'historial_medicamentos': antecedentes_medicos['historialMedicamentos'],
            'historial_enfermedades_familia': antecedentes_medicos['historialEnfermedadesFamilia'],
            'historial_enfermedades_infecciosas': antecedentes_medicos['historialEnfermedadesInfecciosas'],
            'historial_habitos_salud': antecedentes_medicos['historialHabitosSalud']
        })
        if not ant_medicos_serializer.is_valid():
            user.delete()
            usuario_serializer.delete()
            print(ant_medicos_serializer.errors)
            return Response(ant_medicos_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        ant_medicos_serializer.save()
        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)


class UsuarioList(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data)
        usuario_serializer = UsuarioSerializer(data={
            'nombres': data.nombres,
            'primer_apellido': data.primerApellido,
            'segundo_apellido': data.segundoApellido,
            'fecha_nacimiento': data.fechaNacimiento,
            'sexo': data.sexo,
            'altura': data.altura,
            'peso': data.peso,
            'user_id': data.userId})
        if not usuario_serializer.is_valid():
            return Response(usuario_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        usuario_serializer.save()
        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)


class UsuarioDetail(APIView):
    def get_usuario_object(self, user_email):
        try:
            return Usuario.objects.get(email=user_email)
        except Usuario.DoesNotExist:
            raise Http404

    def get_ant_medicos_object(self, id_usuario):
        try:
            return AntecedentesMedicos.objects.get(usuario=id_usuario)
        except AntecedentesMedicos.DoesNotExist:
            raise Http404

    def get(self, request, user_email, format=None):
        usuario = self.get_usuario_object(user_email)
        usuario_pk = usuario.pk
        usuario_serializer = UsuarioSerializer(usuario)
        ant_medicos = self.get_ant_medicos_object(usuario_pk)
        ant_medicos_serializer = AntecedentesMedicosSerializer(ant_medicos)
        response = {'informacion_personal': usuario_serializer.data,
                    'antecedentes_medicos': ant_medicos_serializer.data}
        return Response(response)


class PrediccionList(APIView):
    def get(self, request):
        # prediction data
        predicciones = Prediccion.objects.all()
        predicciones_serializer = PrediccionSerializer(predicciones, many=True)
        predicciones_data = predicciones_serializer.data
        # messages data
        mensajes = Mensaje.objects.all()
        mensajes_serializer = MensajeSerializer(mensajes, many=True)
        mensajes_data = mensajes_serializer.data
        data = []
        for prediccion_data in predicciones_data:
            prediccion = {'mensaje': []}
            for key, value in prediccion_data.items():
                prediccion[key] = value
            for mensaje_data in mensajes_data:
                mensaje = {}
                for key, value in mensaje_data.items():
                    mensaje[key] = value
                if mensaje['prediccion'] == prediccion['id']:
                    prediccion['mensaje'].append(mensaje)
            data.append(prediccion)
        return Response(data)

    def post(self, request):
        data = request.data
        data['enfermedad1']=data['enfermedad1'].split(':')[0]
        data['enfermedad2']=data['enfermedad2'].split(':')[0]
        data['enfermedad3']=data['enfermedad3'].split(':')[0]
        data['enfermedad4']=data['enfermedad4'].split(':')[0]
        data['enfermedad5']=data['enfermedad5'].split(':')[0]
        data['profesional1']=data['profesional1'].split(':')[0]
        data['profesional2']=data['profesional2'].split(':')[0]
        data['profesional3']=data['profesional3'].split(':')[0]
        data['profesional4']=data['profesional4'].split(':')[0]
        data['profesional5']=data['profesional5'].split(':')[0]
        pprint.pprint(data)
        prediccion = Prediccion(usuario=Usuario.objects.get(pk=data['id']),
                                enfermedad1=data['enfermedad1'],
                                enfermedad2=data['enfermedad2'],
                                enfermedad3=data['enfermedad3'],
                                enfermedad4=data['enfermedad4'],
                                enfermedad5=data['enfermedad5'],
                                profesional1=data['profesional1'],
                                profesional2=data['profesional2'],
                                profesional3=data['profesional3'],
                                profesional4=data['profesional4'],
                                profesional5=data['profesional5'])
        prediccion.save()
        mensajes = []
        prediccion_pk = Prediccion.objects.get(pk=prediccion.pk).pk
        for pregunta, respuesta in zip(data['preguntas'], data['respuestas']):
            print((pregunta, respuesta))
            pregunta_serializer = MensajeSerializer(data={
                'prediccion': prediccion_pk,
                'enviado_por_bot': True,
                'texto': pregunta
            })
            if not pregunta_serializer.is_valid():
                print(pregunta_serializer.errors)
                return Response(pregunta_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pregunta_serializer.save()
            respuesta_serializer = MensajeSerializer(data={
                'prediccion': prediccion_pk,
                'enviado_por_bot': False,
                'texto': respuesta
            })
            if not respuesta_serializer.is_valid():
                print(respuesta_serializer.errors)
                return Response(respuesta_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            respuesta_serializer.save()
            par_de_mensajes = {'pregunta': pregunta_serializer.data['texto'],
                               'respuesta': respuesta_serializer.data['texto']}
            mensajes.append(par_de_mensajes)

        return Response({'prediccion_id': prediccion_pk, 'mensajes': mensajes}, status=status.HTTP_201_CREATED)


class PrediccionDetail(APIView):
    def get_predicciones_object(self, id_usuario):
        try:
            print(Prediccion.objects.filter(usuario=id_usuario))
            return Prediccion.objects.filter(usuario=id_usuario)
        except Prediccion.DoesNotExist:
            raise Http404

    def get_mensajes_object(self, id_prediccion):
        try:
            return Mensaje.objects.filter(prediccion=id_prediccion)
        except Mensaje.DoesNotExist:
            raise Http404

    def get(self, request, id_usuario, format=None):
        predicciones = self.get_predicciones_object(id_usuario)
        predicciones_serializer = PrediccionSerializer(predicciones, many=True)
        predicciones_data = predicciones_serializer.data
        data = []
        for prediccion_data in predicciones_data:
            prediccion_auxiliar = {}
            for key, value in prediccion_data.items():
                prediccion_auxiliar[key] = value
            mensajes = self.get_mensajes_object(prediccion_auxiliar['id'])
            mensajes_serializer = MensajeSerializer(mensajes, many=True)
            mensajes_data = mensajes_serializer.data
            prediccion_auxiliar['mensajes'] = []
            for mensaje_data in mensajes_data:
                mensaje_auxiliar = {}
                for key, value in mensaje_data.items():
                    mensaje_auxiliar[key] = value
                prediccion_auxiliar['mensajes'].append(mensaje_auxiliar)
            data.append(prediccion_auxiliar)
        return Response(data)


class GenerarPrediccion(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        ficha_medica = generar_ficha_medica(request.data)
        prediccion = generar_prediccion(ficha_medica)
        # error en la generacion del prediccion
        if 'errorCode' in prediccion.keys():
            print(prediccion)
            return Response(prediccion, status=prediccion['errorStatus'])
        # prediccion OK
        prediccion_list = prediccion['prediccion'].split('\n')
        prediccion_list = list(filter(None, prediccion_list))
        pprint.pprint(prediccion_list)
        data = {'response': prediccion_list[1:6]}
        return Response(data, status=status.HTTP_200_OK)
