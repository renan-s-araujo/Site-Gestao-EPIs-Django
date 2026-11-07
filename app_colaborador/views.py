from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .forms import (
    ColaboradorForm,
    EquipamentoForm,
    EmprestimoForm,
    AtualizarEmprestimoForm,
    CadastroUsuarioForm,
)

from .models import Colaborador, Equipamento, Emprestimo
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# ==========================================
# TELA LOGIN E CADASTRO DE USUÁRIO
# ==========================================



class LoginUsuarioView(auth_views.LoginView):
    template_name = 'protege_mais/login/login.html'
    redirect_authenticated_user = True

def cadastro_usuario(request):
    if request.user.is_authenticated:
        return redirect('lista_colaboradores')

    if request.method == 'POST':
        formulario = CadastroUsuarioForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                'Conta criada com sucesso! Faça login para acessar o sistema.'
            )

            return redirect('login')

    else:
        formulario = CadastroUsuarioForm()

    return render(request, 'protege_mais/login/cadastro.html', {
        'formulario': formulario
    })


# ==========================================
# CRUD DE COLABORADORES
# ==========================================
@login_required
def index(request):
    return render(request, 'protege_mais/base.html')

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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
@login_required
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related(
        'colaborador',
        'equipamento'
    ).all()

    total_emprestimos = emprestimos.count()
    colaborador = request.GET.get('colaborador', '').strip()
    equipamento = request.GET.get('equipamento', '').strip()
    status = request.GET.get('status', '').strip()

    if colaborador:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=colaborador)
    if equipamento:
        emprestimos = emprestimos.filter(equipamento__nome__icontains=equipamento)
    if status in dict(Emprestimo.STATUS):
        emprestimos = emprestimos.filter(status=status)
    else:
        status = ''

    form = EmprestimoForm()
    form_atualizar = AtualizarEmprestimoForm()

    contexto = {
        'emprestimos': emprestimos,
        'total_emprestimos': total_emprestimos,
        'colaborador_filtro': colaborador,
        'equipamento_filtro': equipamento,
        'status_filtro': status,
        'status_opcoes': Emprestimo.STATUS,
        'form': form,
        'form_atualizar': form_atualizar,
    }

    return render(
        request,
        'protege_mais/emprestimos/lista_emprestimos.html',
        contexto
    )

@login_required
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

@login_required
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
