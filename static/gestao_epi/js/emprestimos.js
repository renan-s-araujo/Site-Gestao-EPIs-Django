
document.addEventListener('DOMContentLoaded', () => {
    const cadastro = document.getElementById('emp-modal-cadastro');
    const editar = document.getElementById('emp-modal-editar');

    const modais = [cadastro, editar].filter(Boolean);

    const fechar = modal => {
        modal?.classList.remove('ativo');
    };

    // ========================================
    // CADASTRO DE EMPRÉSTIMO
    // ========================================

    const statusCadastro = document.getElementById('id_status');
    const grupoPrevisao = document.getElementById('emp-grupo-previsao');
    const campoPrevisao = document.getElementById(
        'id_data_prevista_devolucao'
    );

    function atualizarCadastro() {
        const exigePrevisao = statusCadastro?.value === 'Emprestado';

        if (grupoPrevisao) {
            grupoPrevisao.hidden = !exigePrevisao;
        }

        if (campoPrevisao) {
            campoPrevisao.required = exigePrevisao;
        }
    }

    statusCadastro?.addEventListener('change', atualizarCadastro);

    atualizarCadastro();

    // ========================================
    // ATUALIZAÇÃO DE EMPRÉSTIMO
    // ========================================

    const statusEdicao = document.getElementById('emp-editar-status');
    const camposOcorrencia = document.getElementById(
        'emp-campos-ocorrencia'
    );
    const campoData = document.getElementById('emp-editar-data');

    function atualizarEdicao() {
        const mostrar = [
            'Devolvido',
            'Danificado',
            'Perdido'
        ].includes(statusEdicao?.value);

        if (camposOcorrencia) {
            camposOcorrencia.hidden = !mostrar;
        }

        if (campoData) {
            campoData.required = mostrar;
        }
    }

    statusEdicao?.addEventListener('change', atualizarEdicao);

    atualizarEdicao();

    // ========================================
    // ABRIR MODAL DE CADASTRO
    // ========================================

    document.getElementById('emp-abrir-cadastro')
        ?.addEventListener('click', () => {
            cadastro?.classList.add('ativo');
        });

    // ========================================
    // ABRIR MODAL DE EDIÇÃO
    // ========================================

    document.querySelectorAll('.emp-btn-editar').forEach(botao => {
        botao.addEventListener('click', () => {
            const form = document.getElementById('emp-form-editar');

            if (form) {
                form.action = botao.dataset.url;
            }

            document.getElementById(
                'emp-editar-colaborador'
            ).value = botao.dataset.colaborador || '';

            document.getElementById(
                'emp-editar-equipamento'
            ).value = botao.dataset.equipamento || '';

            statusEdicao.value = botao.dataset.status || 'Emprestado';

            campoData.value = botao.dataset.data || '';

            document.getElementById(
                'emp-editar-observacao'
            ).value = botao.dataset.observacao || '';

            atualizarEdicao();

            editar?.classList.add('ativo');
        });
    });

    // Preserva a URL ao retornar erro de validação
    const formEditar = document.getElementById('emp-form-editar');

    if (formEditar?.dataset.errorUrl) {
        formEditar.action = formEditar.dataset.errorUrl;
    }

    // ========================================
    // FECHAR MODAIS PELOS BOTÕES
    // ========================================

    document.querySelectorAll('.emp-fechar').forEach(botao => {
        botao.addEventListener('click', () => {
            const modal = botao.closest('.modal-overlay');

            fechar(modal);
        });
    });

    // ========================================
    // FECHAR AO CLICAR FORA DO MODAL
    // ========================================

    modais.forEach(modal => {
        modal.addEventListener('click', evento => {
            if (evento.target === modal) {
                fechar(modal);
            }
        });
    });

    // ========================================
    // FECHAR COM A TECLA ESC
    // ========================================

    document.addEventListener('keydown', evento => {
        if (evento.key === 'Escape') {
            modais.forEach(fechar);
        }
    });
});
