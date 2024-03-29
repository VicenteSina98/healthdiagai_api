from rest_framework import status
from dotenv import load_dotenv
import os
from openai import OpenAI
import openai
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
from django.template.loader import get_template
import uuid
from django.conf import settings
import xhtml2pdf.pisa as pisa

load_dotenv()
openapi_key = os.getenv('OPENAI_API_KEY')


def generar_parte_inicial() -> str:
    """Le da un rol, la presentacion de la herramienta (ficha medica) y que hacer

    Args:
        ficha_medica (str): ficha medica

    Returns:
        str: ficha medica con las instrucciones agregadas
    """
    ficha_medica = 'Eres un médico general profesional.'
    ficha_medica += ' Te daré los antecedentes médicos de uno de tus pacientes que acudió a una cita médica.'
    ficha_medica += ' Tu tarea es, dados los antecedentes de tu paciente, dar el diagnostico de las 5 patologías con mayor probabilidad de que el paciente las pueda padecer, ordenadas por probabilidad, junto con a qué profesionales recurrir y qué medicamentos utilizar según cada patología.'
    ficha_medica += ' Los antecedentes médicos de tu paciente son los siguientes: '
    return ficha_medica


def calcular_edad(fecha_nacimiento: str) -> str:
    """Calcula la edad de una persona segun fecha de nacimiento

    Args:
        fecha_nacimiento (str): fecha de nacimiento de una persona

    Returns:
        str: edad de la persona
    """
    fecha_nacimiento_split = fecha_nacimiento.split('-')
    year = int(fecha_nacimiento_split[0])
    mes = int(fecha_nacimiento_split[2])
    dia = int(fecha_nacimiento_split[1])
    edad = relativedelta(datetime.now(), datetime(year, dia, mes))
    return str(edad.years)


def concatenar_antecedentes_medicos(ficha_medica: str, antecedentes_medicos: dict) -> str:
    if len(antecedentes_medicos['enfermedades_cronicas']) > 0:
        ficha_medica += 'Padece de las siguientes enfermedades crónicas: '
        ficha_medica += antecedentes_medicos['enfermedades_cronicas'] + '. '
    if len(antecedentes_medicos['historial_alergias']) > 0:
        ficha_medica += 'Es alérgico a: '
        ficha_medica += antecedentes_medicos['historial_alergias'] + '. '
    if len(antecedentes_medicos['historial_cirugias']) > 0:
        ficha_medica += 'Ha sido sometido a las siguientes cirugías: '
        ficha_medica += antecedentes_medicos['historial_cirugias'] + '. '
    if len(antecedentes_medicos['historial_enfermedades_familia']) > 0:
        ficha_medica += 'En su familia es recurrente padecer las siguientes enfermedades: '
        ficha_medica += antecedentes_medicos['historial_enfermedades_familiar'] + '. '
    if len(antecedentes_medicos['historial_enfermedades_infecciosas']) > 0:
        ficha_medica += 'Padece de las siguientes enfermedades infecciosas: '
        ficha_medica += antecedentes_medicos['historial_enfermedades_infecciosas'] + '. '
    if len(antecedentes_medicos['historial_habitos_salud']) > 0:
        ficha_medica += 'Mantiene los siguientes hábitos de salud: '
        ficha_medica += antecedentes_medicos['historial_habitos_salud'] + '. '
    if len(antecedentes_medicos['historial_medicamentos']) > 0:
        ficha_medica += 'Además, ha consumido a lo largo de su vida los siguientes medicamentos: '
        ficha_medica += antecedentes_medicos['historial_medicamentos'] + '. '
    return ficha_medica


def generar_antecedentes_medicos(data: dict, ficha_medica: str) -> str:
    """agrega la informacion personal a la ficha medica

    Args:
        data (dict): informacion personal

    Returns:
        str: ficha medica con la informacion personal agregada
    """
    info_personal = data['informacion_personal']['informacion_personal']
    ant_medicos = data['informacion_personal']['antecedentes_medicos']
    ficha_medica += str(info_personal['nombres']) + ' '
    ficha_medica += str(info_personal['primer_apellido']) + ' '
    ficha_medica += str(info_personal['segundo_apellido']) + ', '
    sexo = ''
    if info_personal['sexo'] == 'M':
        sexo = 'hombre'
    else:
        sexo = 'mujer'

    ficha_medica += sexo + ' de ' + \
        calcular_edad(str(info_personal['fecha_nacimiento'])) + ', '
    ficha_medica += ', ' + \
        str(info_personal['altura']) + ' metros de altura y '
    ficha_medica += str(info_personal['peso']) + ' kilogramos de peso. '
    ficha_medica = concatenar_antecedentes_medicos(ficha_medica, ant_medicos)
    return ficha_medica


def generar_parte_intermedia(ficha_medica: str) -> str:
    ficha_medica += ' La información recopilada en tu cita con el paciente fue la siguiente. '
    return ficha_medica


def generar_informacion_simple(data: dict, key: str, ficha_medica: str, mensaje: str) -> str:
    """agrega la informacion almacenada en data en la llave key a la ficha medica

    Args:
        data (dict): informacion respecto a los datos del paciente
        key (str): llave a buscar en la data
        ficha_medica (str): ficha medica
        mensaje (str): frase para presentar la informacion

    Returns:
        str: ficha medica con la informacion agregada
    """
    ficha_medica += mensaje + data[key] + '. '
    return ficha_medica


def generar_contacto_enfermo(data: dict, ficha_medica: str) -> str:
    """agrega la informacion respecto a contacto con enfermos a la ficha medica

    Args:
        data (dict): informacion respecto a contacto con enfermos
        ficha_medica (str): ficha medica

    Returns:
        str: ficha medica con la informacion agregada
    """
    if not data['ha_tenido_contacto']:
        return ficha_medica
    ficha_medica += 'El paciente ha tenido contacto con algún enfermo. '
    if data['diagnostico'] != None:
        ficha_medica += 'El diagnostico del enfermo es el siguiente: ' + \
            data['diagnostico'] + '. '
    if data['sintomas_relacionados'] != None:
        ficha_medica += 'Los sintomas relacionados con los sintomas del paciente son: ' + \
            data['sintomas_relacionados'] + '. '
    return ficha_medica


def generar_contacto_toxico(data: dict, ficha_medica: str) -> str:
    """agrega la informacion respecto a contacto con agentes infecciosos o toxicos a la ficha medica

    Args:
        data (dict): informacion respecto a contacto con agentes infecciosos o toxicos
        ficha_medica (str): ficha medica

    Returns:
        str: ficha medica con la informacion agregada
    """
    if not data['ha_tenido_contacto']:
        return ficha_medica
    ficha_medica += 'El paciente ha tenido contacto con algún agente infeccioso o tóxico. '
    if data['tipo'] != None:
        ficha_medica += 'El tipo del agente infeccioso o tóxico era del siguiente tipo' + \
            data['tipo']
    return ficha_medica


def generar_viaje_extranjero(data: dict, ficha_medica: str) -> str:
    """agrega la informacion respecto a viajes al extranjero a la ficha medica

    Args:
        data (dict): informacion respecto a viajes al extranjero
        ficha_medica (str): ficha medica

    Returns:
        str: ficha medica con la informacion agregada
    """
    if not data['ha_viajado']:
        return ficha_medica
    if not data['paises']:
        ficha_medica += 'El paciente ha viajado a los siguientes países: ' + \
            data['paises']
    return ficha_medica


def generar_ficha_medica(data: dict, generarParteInicial: bool = True) -> str:
    """genera la ficha medica del paciente

    Args:
        data (dict): informacion a agregar a la ficha medica

    Returns:
        str: ficha medica generada
    """
    ficha_medica = ''
    if generarParteInicial:
        ficha_medica = generar_parte_inicial()
    ficha_medica = generar_antecedentes_medicos(data, ficha_medica)
    ficha_medica = generar_parte_intermedia(ficha_medica)
    ficha_medica = generar_informacion_simple(data, 'sintomas',
                                              ficha_medica, 'El paciente presenta los siguientes sintomas: ')
    ficha_medica = generar_informacion_simple(data, 'consumo_medicamentos',
                                              ficha_medica, 'El paciente consume, de manera regular, los siguientes medicamentos: ')
    ficha_medica = generar_informacion_simple(data, 'estado_animo',
                                              ficha_medica, 'El paciente presenta los siguiente estados de animo: ')
    ficha_medica = generar_contacto_enfermo(
        data['contacto_enfermo'], ficha_medica)
    ficha_medica = generar_viaje_extranjero(
        data['viaje_extranjero'], ficha_medica)
    return ficha_medica


def request_openai(prompt: str) -> dict:
    """genera la prediccion de 5 posibles enfermedades y 5 profesionales a los que recurrir

    Args:
        prompt (str): ficha medica

    Returns:
        dict: prediccion
    """
    try:
        # generar prediccion
        client = OpenAI(api_key=openapi_key)
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )
        # extraer response
        data = {
            'response': completion.choices[0].message.content}
        return data
    except openai.BadRequestError as e:
        data = {'errorCode': 400,
                'errorStatus': status.HTTP_400_BAD_REQUEST,
                'data': e.__dict__}
        return data
    except openai.AuthenticationError as e:
        data = {'errorCode': 401,
                'errorStatus': status.HTTP_401_UNAUTHORIZED,
                'data': e.__dict__}
        return data
    except openai.PermissionDeniedError as e:
        data = {'errorCode': 403,
                'errorStatus': status.HTTP_403_FORBIDDEN,
                'data': e.__dict__}
        return data
    except openai.NotFoundError as e:
        data = {'errorCode': 404,
                'errorStatus': status.HTTP_404_NOT_FOUND,
                'data': e.__dict__}
        return data
    except openai.UnprocessableEntityError as e:
        data = {'errorCode': 422,
                'errorStatus': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'data': e.__dict__}
        return data
    except openai.RateLimitError as e:
        data = {'errorCode': 401,
                'errorStatus': status.HTTP_429,
                'data': e.__dict__}
        return data
    except openai.InternalServerError as e:
        data = {'errorCode': 500,
                'errorStatus': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'data': e.__dict__}
        return data
    except openai.APIConnectionError as e:
        data = {'errorCode': 401,
                'errorStatus': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'data': e.__dict__}
        return data


def clean_prediction(prediction):
    split_prediction = prediction.split('\n')
    split_prediction = split_prediction[1:6]
    remake_prediction = [pred.split(':')[0] for pred in split_prediction]
    return remake_prediction


def save_pdf(params: dict):
    template = get_template('prediction.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    filename = uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR) + f'/public/static/{filename}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)
    if pdf.err:
        return '', False
    return filename, True
