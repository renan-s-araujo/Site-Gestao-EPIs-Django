from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .forms import ColaboradorForm
from .models import Colaborador


def index(request):
    return render(request, 'gestao_epi/base.html')


def lista_colaboradores(request):
    # 1. PROCESSA O ENVIO DO MODAL DE CADASTRO (MÉTODO POST)
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo colaborador no PostgreSQL
            return redirect('lista_colaboradores')  # Recarrega a página limpa
    else:
        form = ColaboradorForm()  # Instancia um formulário em branco para a tela inicial

    # 2. CAPTURA PARÂMETROS DE FILTRO (MÉTODO GET)
    busca = request.GET.get('busca', '').strip()
    setor_selecionado = request.GET.get('setor', '')
    status_selecionado = request.GET.get('status', '')

    # Busca todos os colaboradores cadastrados
    colaboradores = Colaborador.objects.all()

    # Guarda o total geral antes de aplicar os filtros
    total_colaboradores = colaboradores.count()

    # Pesquisa por nome ou matrícula
    # Pesquisa por nome, matrícula ou cargo
    if busca:
        colaboradores = colaboradores.filter(
            Q(nome__icontains=busca)
            | Q(matricula__icontains=busca)
            | Q(cargo__icontains=busca)
        )

    # Filtra por setor
    if setor_selecionado in dict(Colaborador.SETORES):
        colaboradores = colaboradores.filter(
            setor=setor_selecionado
        )

    # Filtra por status
    if status_selecionado in dict(Colaborador.STATUS):
        colaboradores = colaboradores.filter(
            status=status_selecionado
        )

    # 3. CONTEXTO ENVIADO AO TEMPLATE (com a chave 'form' adicionada)
    contexto = {
        'colaboradores': colaboradores,
        'total_colaboradores': total_colaboradores,
        'setores': Colaborador.SETORES,
        'busca': busca,
        'setor_selecionado': setor_selecionado,
        'status_selecionado': status_selecionado,
        'form': form,  # <-- ESTA LINHA FAZ OS CAMPOS DO MODAL APARECEREM
    }

    return render(
        request,
        'gestao_epi/colaboradores/lista_colaboradores.html',
        contexto
    )

@require_POST
def deletar_colaborador(request, pk):
    colaborador = get_object_or_404(Colaborador, pk=pk)
    colaborador.status = 'Inativo'  # Desativa em vez de apagar
    colaborador.save()
    return redirect('lista_colaboradores')

def editar_colaborador(request, pk):
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            colaborador_salvo = form.save(commit=False)
            # Garantia no backend: preserva status e matricula originais imutáveis
            colaborador_salvo.matricula = colaborador.matricula
            colaborador_salvo.status = colaborador.status
            colaborador_salvo.save()
            return redirect('lista_colaboradores')

    # Caso dê algum problema ou se for chamado diretamente, recarrega a lista
    return redirect('lista_colaboradores')