# modulos de django
from django.http import Http404
# modulos de rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# funciones
from healthdiagai.functions import generar_ficha_medica, request_openai, clean_prediction
# modelos
from chat.models import Chat, Mensaje
from api.models import Usuario
# serializers
from chat.serializers import ChatSerializer, MensajeSerializer

# Vistas


class ChatList(APIView):
    def get(self, request):
        # chat data
        chats = Chat.objects.all()
        chats_serializer = ChatSerializer(chats, many=True)
        chats_data = chats_serializer.data
        # messages data
        mensajes = Mensaje.objects.all()
        mensajes_serializer = MensajeSerializer(mensajes, many=True)
        mensajes_data = mensajes_serializer.data
        data = []
        for chat_data in chats_data:
            chat = {'mensaje': []}
            for key, value in chat_data.items():
                chat[key] = value
            for mensaje_data in mensajes_data:
                mensaje = {}
                for key, value in mensaje_data.items():
                    mensaje[key] = value
                if mensaje['chat'] == chat['id']:
                    chat['mensaje'].append(mensaje)
            data.append(chat)
        return Response(data)

    def post(self, request):
        data = request.data
        chat = Chat(usuario=Usuario.objects.get(pk=data['id']),
                    nombre=data['nombre'])
        chat.save()
        mensajes = []
        chat_pk = Chat.objects.get(pk=chat.pk).pk
        if len(data['preguntas']) > len(data['respuestas']):
            data['respuestas'].append('')
        for pregunta, respuesta in zip(data['preguntas'], data['respuestas']):
            par_de_mensajes = {'pregunta': '', 'respuesta': ''}
            pregunta_serializer = MensajeSerializer(data={
                'chat': chat_pk,
                'enviado_por_bot': True,
                'texto': pregunta
            })
            if not pregunta_serializer.is_valid():
                print(pregunta_serializer.errors)
                return Response(pregunta_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pregunta_serializer.save()
            par_de_mensajes['pregunta'] = pregunta_serializer.data['texto']
            if respuesta != '':
                respuesta_serializer = MensajeSerializer(data={
                    'chat': chat_pk,
                    'enviado_por_bot': False,
                    'texto': respuesta
                })
                if not respuesta_serializer.is_valid():
                    print(respuesta_serializer.errors)
                    return Response(respuesta_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                respuesta_serializer.save()
                par_de_mensajes['respuesta'] = respuesta_serializer.data['texto']
            par_de_mensajes['respuesta'] = ''
            mensajes.append(par_de_mensajes)

        return Response({'chat_id': chat_pk, 'mensajes': mensajes}, status=status.HTTP_201_CREATED)


class ChatDetail(APIView):
    def get_chats_object(self, id_usuario):
        try:
            print(Chat.objects.filter(usuario=id_usuario))
            return Chat.objects.filter(usuario=id_usuario)
        except Chat.DoesNotExist:
            raise Http404

    def get_mensajes_object(self, id_chat):
        try:
            return Mensaje.objects.filter(chat=id_chat)
        except Mensaje.DoesNotExist:
            raise Http404

    def get(self, request, id_usuario, format=None):
        chats = self.get_chats_object(id_usuario)
        chats_serializer = ChatSerializer(chats, many=True)
        chats_data = chats_serializer.data
        data = []
        for prediccion_data in chats_data:
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
        prediccion = request_openai(ficha_medica)
        # error en la generacion del prediccion
        if 'errorCode' in prediccion.keys():
            return Response(prediccion, status=prediccion['errorStatus'])
        # prediccion OK
        data = {'response': prediccion['response']}
        return Response(data, status=status.HTTP_200_OK)


class ChatMensaje(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        prompt = 'Eres un médico general profesional. Te daré un listado de posibles enfermedades que le diste a uno de tus pacientes, basándote en una ficha médica del mismo que también te entregaré. '
        prompt += 'Tu tarea es, dada la lista de posibles patologías, responder la siguiente duda de tu paciente: "'
        prompt += request.data['message']
        prompt += '". El listado es el siguiente: '
        prompt += '. '.join(clean_prediction(request.data['prediction']))
        prompt += '. La ficha médica es la siguiente: '
        prompt += generar_ficha_medica(
            request.data['medicalData'], generarParteInicial=False)
        response = request_openai(prompt)
        if 'errorCode' in response.keys():
            return Response(response, status=response['errorStatus'])
        data = {'response': response['response']}
        return Response(data, status=status.HTTP_200_OK)
