# modulos de django
from django.urls import path
# modulos de rest_framework
from rest_framework_simplejwt.views import TokenRefreshView
from user_token.views import MyTokenObtainPairView

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
