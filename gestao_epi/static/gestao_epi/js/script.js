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