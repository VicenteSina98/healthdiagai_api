# modulos de django
from django.urls import path, include
# vistas
from chat.views import ChatList, GenerarPrediccion, ChatDetail, ChatMensaje

urlpatterns = [
    path('', ChatList.as_view()),
    path('generar_prediccion', GenerarPrediccion.as_view()),
    path('guardar', ChatList.as_view()),
    path('historial/<int:id_usuario>', ChatDetail.as_view()),
    path('historial/mensaje', ChatMensaje.as_view()),
]
