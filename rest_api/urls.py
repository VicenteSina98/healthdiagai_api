from django.urls import path
from .views import (
    PrediccionListAPIView
)

urlpatterns = [ 
    path('prediccion', PrediccionListAPIView.as_view())
]
