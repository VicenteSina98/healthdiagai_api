# modulos de django
from django.urls import path, include
# vistas
from api.views import RegisterView, UsuarioDetail, UsuarioList, GeneratePDF

urlpatterns = [
    path('token/', include('user_token.urls')),
    path('chat/', include('chat.urls')),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('usuario', UsuarioList.as_view()),
    path('usuario/<str:user_email>', UsuarioDetail.as_view()),
    path('pdf/<int:id_prediccion>', GeneratePDF.as_view()),
]
