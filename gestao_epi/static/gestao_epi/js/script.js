document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modal-cadastro');
    const btnAbrir = document.getElementById('btn-abrir-modal');
    const btnFecharX = document.getElementById('btn-fechar-x');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Função para abrir o modal
    function abrirModal() {
        if (modal) {
            modal.classList.add('ativo');
        }
    }

    // Função para fechar o modal
    function fecharModal() {
        if (modal) {
            modal.classList.remove('ativo');
        }
    }

    // Eventos de clique
    if (btnAbrir) {
        btnAbrir.addEventListener('click', abrirModal);
    }

    if (btnFecharX) {
        btnFecharX.addEventListener('click', fecharModal);
    }

    if (btnCancelar) {
        btnCancelar.addEventListener('click', fecharModal);
    }

    // Fechar ao clicar fora do cartão branco (no fundo escurecido)
    if (modal) {
        modal.addEventListener('click', function (event) {
            if (event.target === modal) {
                fecharModal();
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // --- MODAL DE CADASTRO ---
    const modalCadastro = document.getElementById('modal-cadastro');
    const btnAbrirCadastro = document.getElementById('btn-abrir-modal');
    const btnFecharXCadastro = document.getElementById('btn-fechar-x');
    const btnCancelarCadastro = document.getElementById('btn-cancelar');

    if (btnAbrirCadastro) btnAbrirCadastro.addEventListener('click', () => modalCadastro.classList.add('ativo'));
    if (btnFecharXCadastro) btnFecharXCadastro.addEventListener('click', () => modalCadastro.classList.remove('ativo'));
    if (btnCancelarCadastro) btnCancelarCadastro.addEventListener('click', () => modalCadastro.classList.remove('ativo'));

    // --- MODAL DE EXCLUSÃO ---
    const modalExcluir = document.getElementById('modal-excluir');
    const btnsAbrirExcluir = document.querySelectorAll('.btn-abrir-modal-excluir');
    const btnCancelarExcluir = document.getElementById('btn-cancelar-excluir');
    const formDeletar = document.getElementById('form-deletar-colaborador');
    const nomeColaboradorSpan = document.getElementById('nome-colaborador-excluir');

    // Ao clicar no botão de excluir da tabela
    btnsAbrirExcluir.forEach(btn => {
        btn.addEventListener('click', function () {
            const url = this.getAttribute('data-url');
            const nome = this.getAttribute('data-nome');

            if (formDeletar) formDeletar.setAttribute('action', url);
            if (nomeColaboradorSpan) nomeColaboradorSpan.textContent = nome;
            if (modalExcluir) modalExcluir.classList.add('ativo');
        });
    });

    if (btnCancelarExcluir) {
        btnCancelarExcluir.addEventListener('click', () => modalExcluir.classList.remove('ativo'));
    }

    // Fechar modais ao clicar no fundo escuro (overlay)
    window.addEventListener('click', function (e) {
        if (e.target === modalCadastro) modalCadastro.classList.remove('ativo');
        if (e.target === modalExcluir) modalExcluir.classList.remove('ativo');
    });
});