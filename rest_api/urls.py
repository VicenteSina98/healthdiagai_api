from django.urls import path
from .views import (
    GenerarPrediccion,
    MyTokenObtainPairView,
    RegisterView,
    UsuarioDetail,
    PrediccionList,
    PrediccionDetail,
    getRoutes
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('usuario/', UsuarioDetail.as_view()),
    path('usuario/<str:user_email>', UsuarioDetail.as_view()),
    path('prediccion/', PrediccionList.as_view()),
    path('prediccion/generar', GenerarPrediccion.as_view()),
    path('prediccion/guardar', PrediccionList.as_view()),
    path('prediccion/<int:id_usuario>', PrediccionDetail.as_view()),
    path('', getRoutes)
]
