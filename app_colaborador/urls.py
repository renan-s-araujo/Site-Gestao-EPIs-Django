from django.urls import path
from . import views

urlpatterns = [
    path( 
        '', views.lista_colaboradores, name='lista_colaboradores' 
        ),

    path(
        'colaboradores/<int:pk>/deletar/', views.deletar_colaborador, name='deletar_colaborador'
        ),

    path(
        'colaboradores/<int:pk>/editar/', views.editar_colaborador, name='editar_colaborador'
        ),

    path(
        'equipamentos/', views.lista_equipamentos, name='lista_equipamentos'
        ),

    path(
    'equipamentos/editar/<str:pk>/',
    views.editar_equipamento,
    name='editar_equipamento'
    ),

    path(
        'equipamentos/deletar/<str:pk>/',
        views.deletar_equipamento,
        name='deletar_equipamento'
    ),
    path(
        'emprestimos/',
        views.lista_emprestimos,
        name='lista_emprestimos'
    ),

    path(
        'emprestimos/cadastrar/',
        views.cadastrar_emprestimo,
        name='cadastrar_emprestimo'
    ),

    path(
        'emprestimos/atualizar/<int:pk>/',
        views.atualizar_emprestimo,
        name='atualizar_emprestimo'
    ),
]
