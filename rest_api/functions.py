from rest_framework import status
from .secret_key import API_KEY
import openai

openai.api_key = API_KEY


def generar_informacion_2D(data: dict, ficha_medica: str, mensaje: str) -> str:
    """agrega la informacion almacenada en data a la ficha medica

    Args:
        data (dict): informacion a agregar a la ficha medica
        ficha_medica (str): ficha medica
        mensaje (str): frase para presentar la informacion

    Returns:
        str: ficha medica con la informacion actualizada
    """
    flag_iteracion = True
    for key, value in data.items():
        if value != None:
            if flag_iteracion:
                # primera iteracion
                ficha_medica += mensaje + key + ': ' + value
                flag_iteracion = False
            else:
                ficha_medica += '; ' + key + ': ' + value
    if not flag_iteracion:
        ficha_medica += '. '
    return ficha_medica


def generar_antecedentes_medicos(data: dict) -> str:
    """agrega la informacion personal a la ficha medica

    Args:
        data (dict): informacion personal

    Returns:
        str: ficha medica con la informacion personal agregada
    """
    personalInfo = data['informacion_personal']
    ficha_medica = 'A continuación se presenta la ficha médica de un paciente. Su nombre es ' + \
        str(personalInfo['nombre'])
    sexo = ''
    if personalInfo['sexo'] == 'M':
        sexo = 'Masculino'
    else:
        sexo = 'Femenino'
    ficha_medica += ', de sexo ' + sexo
    ficha_medica += ', nacido el ' + str(personalInfo['fecha_nacimiento'])
    ficha_medica += ', ' + str(personalInfo['altura']) + ' metros de altura y '
    ficha_medica += str(personalInfo['peso']) + ' kilogramos de peso.'
    ficha_medica = generar_informacion_2D(
        personalInfo['antecedentes_medicos'], ficha_medica, ' Sus antecedentes médicos son los siguientes. ')
    return ficha_medica


def generar_informacion_2D_booleana(data: dict, ficha_medica: str, mensaje: str) -> str:
    """agrega la informacion almacenada en data a la ficha medica

    Args:
        data (dict): informacion a agregar a la ficha medica
        ficha_medica (str): ficha medica
        mensaje (str): frase para presentar la informacion

    Returns:
        str: ficha medica con la informacion actualizada
    """
    flag_iteracion = True
    for key, value in data.items():
        if value != None and value:
            if key == 'otros':
                if flag_iteracion:
                    # primera iteracion
                    ficha_medica += mensaje + key + ': ' + value
                    flag_iteracion = False
                else:
                    ficha_medica += '; ' + key + ': ' + value
            else:
                if flag_iteracion:
                    # primera iteracion
                    ficha_medica += mensaje + key
                    flag_iteracion = False
                else:
                    ficha_medica += ',  ' + key
    if not flag_iteracion:
        ficha_medica += '. '
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
        ficha_medica += 'Los sintomas relacionados son: ' + \
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


def generar_parte_final(ficha_medica: str) -> str:
    """agrega las instrucciones para que ChatGPT genere la prediccion

    Args:
        ficha_medica (str): ficha medica

    Returns:
        str: ficha medica con las instrucciones agregadas
    """
    ficha_medica += 'Necesito que, según la ficha médica presentada, y me des un listado de las 5 enfermedades con mas probabilidad de que el paciente esté enfermo, junto a una breve explicación del porqué es posible que tenga dicha enfermedad. '
    ficha_medica += 'Además, necesito que me des un listado de los profesionales del área de la salud a los cuales el paciente puede recurrir para atenderse según su ficha médica y las 5 posibles enfermedades pedidas anteriormente.'
    return ficha_medica


def generar_ficha_medica(data: dict) -> str:
    """genera la ficha medica del paciente

    Args:
        data (dict): informacion a agregar a la ficha medica

    Returns:
        str: ficha medica generada
    """
    print(data)
    ficha_medica = generar_antecedentes_medicos(data)
    ficha_medica = generar_informacion_simple(data, 'alergias_medicamentos',
                                              ficha_medica, 'El paciente es alergico a los siguientes medicamentos: ')
    ficha_medica = generar_informacion_simple(data, 'alergias_alimentos',
                                              ficha_medica, 'El paciente es alergico a los siguientes alimentos: ')
    ficha_medica = generar_informacion_simple(data, 'sintomas',
                                              ficha_medica, 'El paciente presenta los siguientes sintomas: ')
    ficha_medica = generar_informacion_simple(data, 'consumo_medicamentos',
                                              ficha_medica, 'El paciente consume los siguientes medicamentos: ')
    ficha_medica = generar_informacion_simple(data, 'estado_animo',
                                              ficha_medica, 'El paciente presenta los siguiente estados de animo: ')
    ficha_medica = generar_contacto_enfermo(
        data['contacto_enfermo'], ficha_medica)
    ficha_medica = generar_viaje_extranjero(
        data['viaje_extranjero'], ficha_medica)
    ficha_medica = generar_parte_final(ficha_medica)
    return ficha_medica


def generar_prediccion(ficha_medica: str) -> dict:
    """genera la prediccion de 5 posibles enfermedades y 5 profesionales a los que recurrir

    Args:
        ficha_medica (str): ficha medica

    Returns:
        dict: prediccion
    """
    try:
        # generar prediccion
        prediccion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': ficha_medica}
            ],
            temperature=0
        )
        # extraer prediccion
        data = {
            'prediccion': prediccion['choices'][0]['message']['content']}
        return data
    except Exception as e:
        data = {'errorCode': 503,
                'errorStatus': status.HTTP_503__SERVICE_UNAVAILABLE}
        return data
