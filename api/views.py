# libreria
from datetime import datetime
# modulos de django
from django.contrib.auth.models import User
from django.http import Http404
# modulos de rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# funciones
from healthdiagai.functions import save_pdf
# modelos
from api.models import Usuario, AntecedentesMedicos
from chat.models import Chat, Mensaje
# serializers
from api.serializers import UsuarioSerializer, AntecedentesMedicosSerializer

# Vistas


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


class GeneratePDF(APIView):
    def get(self, request, id_prediccion):
        prediction = Chat.objects.get(id=id_prediccion)
        messages = Mensaje.objects.filter(prediccion=id_prediccion)
        params = {
            'today': datetime.now(),
            'prediction': prediction,
            'messages': messages,
        }
        file_name, status = save_pdf(params)
        if not status:
            return Response({'status': 400})
        return Response({'status': 200, 'path': f'/media/{file_name}.pdf'})
