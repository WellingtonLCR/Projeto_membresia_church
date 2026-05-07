document.querySelectorAll('.btn-excluir').forEach((botao) => {
    botao.addEventListener('click', (evento) => {
        const mensagem = botao.dataset.confirmMessage || 'Tem certeza que deseja excluir este registro?';
        const confirmou = window.confirm(mensagem);

        if (!confirmou) {
            evento.preventDefault();
        }
    });
});

const campoSenha = document.getElementById('senha');
const forcaSenha = document.getElementById('forca-senha');

if (campoSenha && forcaSenha) {
    campoSenha.addEventListener('input', () => {
        const valor = campoSenha.value;
        let nivel = 'Senha fraca';
        let classe = 'is-weak';

        if (valor.length >= 8 && /[A-Z]/.test(valor) && /\d/.test(valor)) {
            nivel = 'Senha forte';
            classe = 'is-strong';
        } else if (valor.length >= 8 || (valor.length >= 6 && /\d/.test(valor))) {
            nivel = 'Senha média';
            classe = 'is-medium';
        }

        forcaSenha.classList.remove('is-weak', 'is-medium', 'is-strong');
        forcaSenha.classList.add(classe);
        forcaSenha.textContent = `Força da senha: ${nivel}`;
    });
}
