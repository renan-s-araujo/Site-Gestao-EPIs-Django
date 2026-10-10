from django.urls import path
from . import views

urlpatterns = [
    path( '', views.lista_colaboradores, name='lista_colaboradores' ),
    path('colaboradores/<int:pk>/deletar/', views.deletar_colaborador, name='deletar_colaborador'),
]
