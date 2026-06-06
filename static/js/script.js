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

document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const atualizarRadioCards = (input) => {
        const form = input.closest('form') || document;
        const grupo = form.querySelectorAll(`input[type="radio"][name="${input.name}"]`);

        grupo.forEach((radio) => {
            const card = radio.closest('.radio-card');
            if (!card) {
                return;
            }

            const selecionado = radio.checked;
            card.classList.toggle('selected', selecionado);
            card.classList.toggle('is-selected', selecionado);
        });
    };

    document.querySelectorAll('.radio-card input[type="radio"]').forEach((input) => {
        atualizarRadioCards(input);
        input.addEventListener('change', () => atualizarRadioCards(input));
    });

    const tipoIdentificador = document.querySelector('select[name="identificador_tipo"]');
    const identificador = document.querySelector('input[name="identificador"]');

    if (tipoIdentificador && identificador) {
        const placeholders = {
            email: 'domuschurchapp@gmail.com',
            celular: '(00) 00000-0000',
            cpf: '000.000.000-00',
            username: 'admin.domus',
        };

        const atualizarPlaceholder = () => {
            identificador.placeholder = placeholders[tipoIdentificador.value] || 'Digite seu identificador';
        };

        tipoIdentificador.addEventListener('change', atualizarPlaceholder);
        atualizarPlaceholder();
    }

    const doadorRadios = document.querySelectorAll('input[name="doador_tipo"]');
    const campoMembro = document.querySelector('.field-member');
    const selectMembro = document.getElementById('membroDoacao');
    const campoNomeDoador = document.querySelector('.field-donor-name');
    const inputNomeDoador = document.getElementById('doadorNome');

    const atualizarDoador = () => {
        const selecionado = document.querySelector('input[name="doador_tipo"]:checked');
        const tipo = selecionado ? selecionado.value : 'membro';

        if (campoMembro) {
            campoMembro.classList.toggle('d-none', tipo !== 'membro');
        }

        if (campoNomeDoador) {
            campoNomeDoador.classList.toggle('d-none', tipo === 'anonimo');
        }

        if (tipo !== 'membro' && selectMembro) {
            selectMembro.value = '';
        }

        if (inputNomeDoador) {
            if (tipo === 'anonimo') {
                inputNomeDoador.value = 'Anonimo';
            } else if (inputNomeDoador.value === 'Anonimo') {
                inputNomeDoador.value = '';
            }
        }
    };

    doadorRadios.forEach((radio) => {
        radio.addEventListener('change', atualizarDoador);
    });
    atualizarDoador();
});
