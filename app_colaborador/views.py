from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .forms import (
    ColaboradorForm,
    EquipamentoForm,
    EmprestimoForm,
    AtualizarEmprestimoForm,
)

from .models import Colaborador, Equipamento, Emprestimo


# ==========================================
# TELA INICIAL
# ==========================================

def index(request):
    return render(request, 'protege_mais/base.html')


# ==========================================
# CRUD DE COLABORADORES
# ==========================================

def lista_colaboradores(request):

    # 1. CADASTRO DE COLABORADORES
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Colaborador cadastrado com sucesso!'
            )
            return redirect('lista_colaboradores')
        else:
            messages.error(
                request,
                'Erro ao cadastrar colaborador. Verifique os campos.'
            )
    else:
        form = ColaboradorForm()

    # 2. FILTROS DE PESQUISA
    busca = request.GET.get('busca', '').strip()
    setor_selecionado = request.GET.get('setor', '')
    status_selecionado = request.GET.get('status', '')

    colaboradores = Colaborador.objects.all()
    total_colaboradores = colaboradores.count()

    if busca:
        colaboradores = colaboradores.filter(
            Q(nome__icontains=busca)
            | Q(matricula__icontains=busca)
            | Q(cargo__icontains=busca)
        )

    if setor_selecionado in dict(Colaborador.SETORES):
        colaboradores = colaboradores.filter(
            setor=setor_selecionado
        )

    if status_selecionado in dict(Colaborador.STATUS):
        colaboradores = colaboradores.filter(
            status=status_selecionado
        )

    contexto = {
        'colaboradores': colaboradores,
        'total_colaboradores': total_colaboradores,
        'setores': Colaborador.SETORES,
        'busca': busca,
        'setor_selecionado': setor_selecionado,
        'status_selecionado': status_selecionado,
        'form': form,
    }

    return render(
        request,
        'protege_mais/colaboradores/lista_colaboradores.html',
        contexto
    )


@require_POST
def deletar_colaborador(request, pk):

    colaborador = get_object_or_404(Colaborador, pk=pk)

    # Desativa o colaborador sem apagar seu registro
    colaborador.status = 'Inativo'
    colaborador.save()

    messages.success(
        request,
        'Colaborador desativado com sucesso!'
    )

    return redirect('lista_colaboradores')


def editar_colaborador(request, pk):

    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        form = ColaboradorForm(
            request.POST,
            instance=colaborador
        )

        if form.is_valid():
            colaborador_salvo = form.save(commit=False)

            # Preserva matrícula e status
            colaborador_salvo.matricula = colaborador.matricula
            colaborador_salvo.status = colaborador.status

            colaborador_salvo.save()

            messages.success(
                request,
                'Colaborador atualizado com sucesso!'
            )

            return redirect('lista_colaboradores')

        messages.error(
            request,
            'Erro ao atualizar colaborador.'
        )

    return redirect('lista_colaboradores')


# ==========================================
# CRUD DE EQUIPAMENTOS
# ==========================================

def lista_equipamentos(request):

    # 1. CADASTRO DE EQUIPAMENTOS
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Equipamento cadastrado com sucesso!'
            )

            return redirect('lista_equipamentos')

        else:
            messages.error(
                request,
                'Erro ao cadastrar equipamento. Verifique os campos.'
            )

    else:
        form = EquipamentoForm()

    # 2. LISTAGEM DOS EQUIPAMENTOS
    equipamentos = Equipamento.objects.all()

    total_equipamentos = equipamentos.count()

    # 3. PESQUISA POR NOME OU CA
    busca = request.GET.get('busca', '').strip()

    if busca:
        equipamentos = equipamentos.filter(
            Q(nome__icontains=busca)
            | Q(ca__icontains=busca)
        )

    # 4. CONTEXTO PARA O TEMPLATE
    contexto = {
        'equipamentos': equipamentos,
        'total_equipamentos': total_equipamentos,
        'busca': busca,
        'form': form,
    }

    return render(
        request,
        'protege_mais/equipamentos/lista_equipamentos.html',
        contexto
    )


@require_POST
def editar_equipamento(request, pk):

    equipamento = get_object_or_404(
        Equipamento,
        pk=pk
    )

    form = EquipamentoForm(
        request.POST,
        instance=equipamento
    )

    # Impede alteração do CA, que é a chave primária
    form.fields['ca'].disabled = True

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Equipamento atualizado com sucesso!'
        )
    else:
        messages.error(
            request,
            'Erro ao atualizar equipamento. Verifique os campos.'
        )

    return redirect('lista_equipamentos')


@require_POST
def deletar_equipamento(request, pk):

    equipamento = get_object_or_404(
        Equipamento,
        pk=pk
    )

    equipamento.status = 'Inativo'
    equipamento.save()

    messages.success(
        request,
        'Equipamento excluído com sucesso!'
    )

    return redirect('lista_equipamentos')



# ========================================
# EMPRÉSTIMOS DE EPIs
# ========================================

def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related(
        'colaborador',
        'equipamento'
    ).all()

    form = EmprestimoForm()
    form_atualizar = AtualizarEmprestimoForm()

    contexto = {
        'emprestimos': emprestimos,
        'total_emprestimos': emprestimos.count(),
        'form': form,
        'form_atualizar': form_atualizar,
    }

    return render(
        request,
        'protege_mais/emprestimos/lista_emprestimos.html',
        contexto
    )


@require_POST
def cadastrar_emprestimo(request):
    form = EmprestimoForm(request.POST)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Empréstimo cadastrado com sucesso!'
        )
    else:
        messages.error(
            request,
            'Erro ao cadastrar empréstimo. Verifique os dados informados.'
        )

    return redirect('lista_emprestimos')


@require_POST
def atualizar_emprestimo(request, pk):
    emprestimo = get_object_or_404(
        Emprestimo,
        pk=pk
    )

    form = AtualizarEmprestimoForm(
        request.POST,
        instance=emprestimo
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Status do empréstimo atualizado com sucesso!'
        )
    else:
        messages.error(
            request,
            'Erro ao atualizar empréstimo. Verifique os dados.'
        )

    return redirect('lista_emprestimos')
