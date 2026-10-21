document.addEventListener('DOMContentLoaded', function () {

    // ========================================
    // 1. MODAL DE CADASTRO
    // ========================================
    const modalCadastro = document.getElementById('modal-cadastro');
    const btnAbrirCadastro = document.getElementById('btn-abrir-modal');
    const btnFecharXCadastro = document.getElementById('btn-fechar-x');
    const btnCancelarCadastro = document.getElementById('btn-cancelar');

    if (btnAbrirCadastro && modalCadastro) {
        btnAbrirCadastro.addEventListener('click', () => modalCadastro.classList.add('ativo'));
    }
    if (btnFecharXCadastro && modalCadastro) {
        btnFecharXCadastro.addEventListener('click', () => modalCadastro.classList.remove('ativo'));
    }
    if (btnCancelarCadastro && modalCadastro) {
        btnCancelarCadastro.addEventListener('click', () => modalCadastro.classList.remove('ativo'));
    }


    // ========================================
    // 2. MODAL DE EDIÇÃO
    // ========================================
    const modalEditar = document.getElementById('modal-editar');
    const btnsEditar = document.querySelectorAll('.btn-abrir-modal-editar');
    const btnFecharXEditar = document.getElementById('btn-fechar-x-editar');
    const btnCancelarEditar = document.getElementById('btn-cancelar-editar');
    const formEditar = document.getElementById('form-editar-colaborador');

    btnsEditar.forEach(btn => {
        btn.addEventListener('click', function () {
            if (!modalEditar) return;

            // Atualiza a URL do formulário
            const url = this.getAttribute('data-url');
            if (formEditar && url) {
                formEditar.setAttribute('action', url);
            }

            // Preenche os campos travados (se existirem no modal)
            const elMatricula = document.getElementById('editar-matricula');
            const elStatus = document.getElementById('editar-status');
            const elNome = document.getElementById('editar-nome');
            const elCargo = document.getElementById('editar-cargo');
            const elSetor = document.getElementById('editar-setor');

            if (elMatricula) elMatricula.value = this.getAttribute('data-matricula') || '';
            if (elStatus) elStatus.value = this.getAttribute('data-status') || '';
            if (elNome) elNome.value = this.getAttribute('data-nome') || '';
            if (elCargo) elCargo.value = this.getAttribute('data-cargo') || '';
            if (elSetor) elSetor.value = this.getAttribute('data-setor') || '';

            modalEditar.classList.add('ativo');
        });
    });

    if (btnFecharXEditar && modalEditar) {
        btnFecharXEditar.addEventListener('click', () => modalEditar.classList.remove('ativo'));
    }
    if (btnCancelarEditar && modalEditar) {
        btnCancelarEditar.addEventListener('click', () => modalEditar.classList.remove('ativo'));
    }


    // ========================================
    // 3. MODAL DE EXCLUSÃO
    // ========================================
    const modalExcluir = document.getElementById('modal-excluir');
    const btnsExcluir = document.querySelectorAll('.btn-abrir-modal-excluir');
    const btnCancelarExcluir = document.getElementById('btn-cancelar-excluir');
    const formExcluir = document.getElementById('form-deletar-colaborador');
    const nomeExcluirSpan = document.getElementById('nome-colaborador-excluir');

    btnsExcluir.forEach(btn => {
        btn.addEventListener('click', function () {
            if (!modalExcluir) return;

            const url = this.getAttribute('data-url');
            const nome = this.getAttribute('data-nome');

            if (formExcluir && url) formExcluir.setAttribute('action', url);
            if (nomeExcluirSpan && nome) nomeExcluirSpan.textContent = nome;

            modalExcluir.classList.add('ativo');
        });
    });

    if (btnCancelarExcluir && modalExcluir) {
        btnCancelarExcluir.addEventListener('click', () => modalExcluir.classList.remove('ativo'));
    }


    // ========================================
    // 4. FECHAR MODAIS AO CLICAR NO OVERLAY (FUNDO)
    // ========================================
    window.addEventListener('click', function (e) {
        if (e.target === modalCadastro) modalCadastro.classList.remove('ativo');
        if (e.target === modalEditar) modalEditar.classList.remove('ativo');
        if (e.target === modalExcluir) modalExcluir.classList.remove('ativo');
    });

});