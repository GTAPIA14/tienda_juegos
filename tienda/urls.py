
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path(
        'juego/<int:juego_id>/',
        views.detalle_juego,
        name='detalle_juego'
    ),

    path(
        'comprobante/<str:codigo>/',
        views.comprobante,
        name='comprobante'
    ),
]
