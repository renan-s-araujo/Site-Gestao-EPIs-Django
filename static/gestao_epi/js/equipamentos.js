document.addEventListener('DOMContentLoaded', () => {
    const cadastro = document.getElementById('epi-modal-cadastro');
    const editar = document.getElementById('epi-modal-editar');
    const excluir = document.getElementById('epi-modal-excluir');
    const modais = [cadastro, editar, excluir].filter(Boolean);
    const fechar = modal => modal.classList.remove('ativo');

    document.getElementById('epi-abrir-cadastro')?.addEventListener('click', () => cadastro?.classList.add('ativo'));

    document.querySelectorAll('.epi-btn-editar').forEach(botao => {
        botao.addEventListener('click', () => {
            const form = document.getElementById('epi-form-editar');
            form.action = botao.dataset.url;
            document.getElementById('epi-editar-ca').value = botao.dataset.ca || '';
            document.getElementById('epi-editar-nome').value = botao.dataset.nome || '';
            document.getElementById('epi-editar-tipo').value = botao.dataset.tipo || '';
            document.getElementById('epi-editar-status').value = botao.dataset.status || '';
            document.getElementById('epi-editar-quantidade').value = botao.dataset.quantidade || '0';
            editar.classList.add('ativo');
        });
    });

    document.querySelectorAll('.epi-btn-excluir').forEach(botao => {
        botao.addEventListener('click', () => {
            document.getElementById('epi-form-excluir').action = botao.dataset.url;
            document.getElementById('epi-nome-excluir').textContent = botao.dataset.nome || '';
            excluir.classList.add('ativo');
        });
    });

    document.querySelectorAll('.epi-fechar').forEach(botao => {
        botao.addEventListener('click', () => {
            const modal = botao.closest('.modal-overlay');
            if (modal) fechar(modal);
        });
    });
    modais.forEach(modal => modal.addEventListener('click', evento => {
        if (evento.target === modal) fechar(modal);
    }));
    document.addEventListener('keydown', evento => {
        if (evento.key === 'Escape') modais.forEach(fechar);
    });
});
