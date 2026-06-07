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
    document.body.classList.add('ui-ready');

    const atualizarIcones = () => {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    };

    if (window.lucide) {
        atualizarIcones();
    } else {
        document.querySelectorAll('[data-lucide]').forEach((icone) => {
            icone.setAttribute('aria-hidden', 'true');
            icone.classList.add('icon-fallback');
        });
    }

    const CHAVE_TEMA = 'membresia-theme';
    const temaAtual = () => document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const aplicarTema = (tema) => {
        const temaNormalizado = tema === 'dark' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', temaNormalizado);
        document.body.dataset.theme = temaNormalizado;

        document.querySelectorAll('[data-theme-toggle]').forEach((botao) => {
            const escuro = temaNormalizado === 'dark';
            botao.setAttribute('aria-pressed', String(escuro));
            botao.setAttribute('title', escuro ? 'Ativar modo claro' : 'Ativar modo escuro');
            botao.setAttribute('aria-label', escuro ? 'Ativar modo claro' : 'Ativar modo escuro');
            botao.innerHTML = `<i data-lucide="${escuro ? 'sun' : 'moon'}"></i>`;
        });

        atualizarIcones();
    };

    aplicarTema(temaAtual());

    document.querySelectorAll('[data-theme-toggle]').forEach((botao) => {
        botao.addEventListener('click', () => {
            const proximoTema = temaAtual() === 'dark' ? 'light' : 'dark';
            try {
                localStorage.setItem(CHAVE_TEMA, proximoTema);
            } catch (erro) {
                // Preferimos manter a troca visual mesmo se o navegador bloquear storage.
            }
            aplicarTema(proximoTema);
        });
    });

    const garantirBackdrop = () => {
        let backdrop = document.querySelector('.membresia-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('button');
            backdrop.type = 'button';
            backdrop.className = 'membresia-backdrop';
            backdrop.setAttribute('aria-label', 'Fechar painel');
            document.body.appendChild(backdrop);
        }
        return backdrop;
    };

    const overlayAberto = () => document.querySelector('.modal.show, .modal.is-open, .offcanvas.show, .offcanvas.is-open');

    const liberarPagina = () => {
        document.querySelectorAll('.membresia-backdrop, .modal-backdrop').forEach((backdrop) => backdrop.remove());
        document.body.classList.remove('membresia-overlay-open', 'modal-open');
        document.body.style.removeProperty('overflow');
        document.body.style.removeProperty('padding-right');
    };

    const limparTravamentoOverlay = () => {
        window.setTimeout(() => {
            if (!overlayAberto()) {
                liberarPagina();
            }
        }, 80);
    };

    const fecharOverlay = () => {
        document.querySelectorAll('.modal.is-open, .offcanvas.is-open').forEach((elemento) => {
            elemento.classList.remove('is-open', 'show');
            elemento.setAttribute('aria-hidden', 'true');
        });

        liberarPagina();
    };

    const abrirOverlay = (alvo) => {
        if (!alvo) {
            return;
        }

        alvo.classList.add('is-open', 'show');
        alvo.removeAttribute('aria-hidden');
        document.body.classList.add('membresia-overlay-open');
        garantirBackdrop().addEventListener('click', fecharOverlay, { once: true });

        const campoFoco = alvo.querySelector('input, select, textarea, button:not(.btn-close)');
        if (campoFoco) {
            window.setTimeout(() => campoFoco.focus(), 80);
        }
    };

    document.querySelectorAll('.modal, .offcanvas').forEach((elemento) => {
        elemento.addEventListener('hidden.bs.modal', limparTravamentoOverlay);
        elemento.addEventListener('hidden.bs.offcanvas', limparTravamentoOverlay);
    });

    document.querySelectorAll('[data-bs-dismiss="modal"], [data-bs-dismiss="offcanvas"], .btn-close').forEach((botao) => {
        botao.addEventListener('click', () => {
            window.setTimeout(limparTravamentoOverlay, 250);
        });
    });

    document.querySelectorAll('[data-bs-toggle="modal"], [data-bs-toggle="offcanvas"]').forEach((botao) => {
        botao.addEventListener('click', (evento) => {
            const seletor = botao.getAttribute('data-bs-target') || botao.getAttribute('href');
            const alvo = seletor ? document.querySelector(seletor) : null;

            if (!alvo) {
                return;
            }

            if (!window.bootstrap) {
                evento.preventDefault();
                abrirOverlay(alvo);
                return;
            }

            window.setTimeout(() => {
                if (!alvo.classList.contains('show')) {
                    const instancia = alvo.classList.contains('offcanvas')
                        ? window.bootstrap.Offcanvas.getOrCreateInstance(alvo)
                        : window.bootstrap.Modal.getOrCreateInstance(alvo);
                    instancia.show();
                }
            }, 120);
        });
    });

    document.addEventListener('keydown', (evento) => {
        if (evento.key === 'Escape') {
            if (document.querySelector('.modal.is-open, .offcanvas.is-open')) {
                fecharOverlay();
            } else {
                limparTravamentoOverlay();
            }
        }
    });

    document.querySelectorAll('.admin-brand .icon-button[aria-label*="Recolher"]').forEach((botao) => {
        botao.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-collapsed');
        });
    });

    document.addEventListener('keydown', (evento) => {
        if ((evento.ctrlKey || evento.metaKey) && evento.key.toLowerCase() === 'k') {
            const busca = document.querySelector('.admin-search input');
            if (busca) {
                evento.preventDefault();
                busca.focus();
            }
        }
    });

    const normalizarTexto = (texto) => texto
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .trim();

    const buscaTopo = document.querySelector('[data-local-search] input');

    if (buscaTopo) {
        const tabelaAtual = document.querySelector('.admin-table tbody');
        const linhasTabela = tabelaAtual ? Array.from(tabelaAtual.querySelectorAll('tr')) : [];
        const cardsBuscaveis = Array.from(document.querySelectorAll('.metric-card, .content-card'))
            .filter((card) => !card.closest('.modal, .offcanvas'));
        const alvoBusca = tabelaAtual || document.querySelector('.admin-page');

        let avisoVazio = document.querySelector('.local-search-empty');
        if (alvoBusca && !avisoVazio) {
            avisoVazio = document.createElement('div');
            avisoVazio.className = 'local-search-empty';
            avisoVazio.textContent = 'Nenhum resultado encontrado para a busca atual.';
            alvoBusca.insertAdjacentElement(tabelaAtual ? 'afterend' : 'beforeend', avisoVazio);
        }

        const aplicarBusca = () => {
            const termo = normalizarTexto(buscaTopo.value);
            let visiveis = 0;

            if (linhasTabela.length) {
                linhasTabela.forEach((linha) => {
                    const texto = normalizarTexto(linha.textContent || '');
                    const ehVazio = Boolean(linha.querySelector('.empty-state'));
                    const mostrar = !termo || ehVazio || texto.includes(termo);
                    linha.classList.toggle('local-search-hidden', !mostrar);
                    if (mostrar && !ehVazio) {
                        visiveis += 1;
                    }
                });
            } else {
                cardsBuscaveis.forEach((card) => {
                    const mostrar = !termo || normalizarTexto(card.textContent || '').includes(termo);
                    card.classList.toggle('local-search-hidden', !mostrar);
                    if (mostrar) {
                        visiveis += 1;
                    }
                });
            }

            if (avisoVazio) {
                avisoVazio.classList.toggle('is-visible', Boolean(termo) && visiveis === 0);
            }
        };

        buscaTopo.addEventListener('input', aplicarBusca);
        buscaTopo.addEventListener('search', aplicarBusca);
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
            email: 'admin@igreja.org',
            celular: '(00) 00000-0000',
            cpf: '000.000.000-00',
            username: 'admin.igreja',
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

    document.querySelectorAll('.money-input').forEach((input) => {
        input.addEventListener('input', () => {
            const numeros = input.value.replace(/\D/g, '');
            if (!numeros) {
                input.value = '';
                return;
            }

            const valor = Number(numeros) / 100;
            input.value = valor.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL',
            });
        });
    });
});
