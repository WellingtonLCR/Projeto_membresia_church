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
    const TEMAS_VALIDOS = ['light', 'dark', 'contrast', 'system'];
    const temaSistemaEscuro = () => window.matchMedia
        && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const lerTemaPreferido = () => {
        try {
            const temaSalvo = localStorage.getItem(CHAVE_TEMA) || 'light';
            return TEMAS_VALIDOS.includes(temaSalvo) ? temaSalvo : 'light';
        } catch (erro) {
            return 'light';
        }
    };
    const temaAplicado = (preferencia) => {
        if (preferencia === 'system') {
            return temaSistemaEscuro() ? 'dark' : 'light';
        }
        return preferencia;
    };
    const iconeTema = {
        light: 'sun',
        dark: 'moon',
        contrast: 'eye',
        system: 'monitor',
    };
    const rotuloTema = {
        light: 'Claro',
        dark: 'Escuro',
        contrast: 'Alto contraste',
        system: 'Sistema',
    };
    const aplicarTema = (preferencia) => {
        const temaPreferido = TEMAS_VALIDOS.includes(preferencia) ? preferencia : 'light';
        const temaVisual = temaAplicado(temaPreferido);

        document.documentElement.setAttribute('data-theme', temaVisual);
        document.documentElement.setAttribute('data-theme-choice', temaPreferido);
        document.body.dataset.theme = temaVisual;

        document.querySelectorAll('[data-theme-toggle]').forEach((botao) => {
            botao.setAttribute('aria-pressed', String(temaVisual !== 'light'));
            botao.setAttribute('title', `Aparencia: ${rotuloTema[temaPreferido]}`);
            botao.setAttribute('aria-label', `Aparencia atual: ${rotuloTema[temaPreferido]}`);
            botao.innerHTML = `<i data-lucide="${iconeTema[temaPreferido]}"></i>`;
        });

        document.querySelectorAll('[data-theme-option]').forEach((opcao) => {
            const ativo = opcao.dataset.themeOption === temaPreferido;
            opcao.classList.toggle('active', ativo);
            opcao.setAttribute('aria-pressed', String(ativo));
        });

        atualizarIcones();
    };

    let temaPreferidoAtual = lerTemaPreferido();
    aplicarTema(temaPreferidoAtual);

    document.querySelectorAll('[data-theme-option]').forEach((opcao) => {
        opcao.addEventListener('click', () => {
            const proximoTema = opcao.dataset.themeOption;
            if (!TEMAS_VALIDOS.includes(proximoTema)) {
                return;
            }

            temaPreferidoAtual = proximoTema;
            try {
                localStorage.setItem(CHAVE_TEMA, proximoTema);
            } catch (erro) {
                // Preferimos manter a troca visual mesmo se o navegador bloquear storage.
            }
            aplicarTema(proximoTema);
        });
    });

    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
            if (temaPreferidoAtual === 'system') {
                aplicarTema('system');
            }
        });
    }

    const garantirBackdrop = () => {
        let backdrop = document.querySelector('.membresia-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('button');
            backdrop.type = 'button';
            backdrop.className = 'membresia-backdrop';
            backdrop.setAttribute('aria-label', 'Fechar painel');
            document.body.appendChild(backdrop);
        }
        backdrop.style.setProperty('z-index', '1080', 'important');
        return backdrop;
    };

    const removerBackdropLocal = () => {
        document.querySelectorAll('.membresia-backdrop').forEach((backdrop) => backdrop.remove());
        document.body.classList.remove('membresia-overlay-open');
    };

    const bootstrapModalAtivo = () => document.querySelector('.modal.show');
    const bootstrapOffcanvasAtivo = () => document.querySelector('.offcanvas.show');
    const overlayCustomAtivo = () => document.querySelector('.modal.is-open, .offcanvas.is-open');
    const overlayAberto = () => bootstrapModalAtivo() || bootstrapOffcanvasAtivo() || overlayCustomAtivo();

    const limparBackdropsOrfaos = () => {
        const existeBootstrap = bootstrapModalAtivo() || bootstrapOffcanvasAtivo();
        const existeCustom = overlayCustomAtivo();

        document.querySelectorAll('.membresia-backdrop').forEach((backdrop) => backdrop.remove());

        if (!existeBootstrap && !existeCustom) {
            document.querySelectorAll('.modal-backdrop').forEach((backdrop) => backdrop.remove());
        }
    };

    const liberarPagina = () => {
        const existeBootstrap = bootstrapModalAtivo() || bootstrapOffcanvasAtivo();
        const existeCustom = overlayCustomAtivo();

        limparBackdropsOrfaos();

        if (!existeCustom) {
            document.body.classList.remove('membresia-overlay-open');
        }

        if (!existeBootstrap) {
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('overflow');
            document.body.style.removeProperty('padding-right');
        }
    };

    const prepararInteracaoModal = (modal) => {
        modal.removeAttribute('aria-hidden');
        modal.style.pointerEvents = 'auto';

        modal.querySelectorAll('.modal-dialog, .modal-content, .modal-body, form, input, select, textarea, button, a, [role="button"], [tabindex]').forEach((elemento) => {
            elemento.style.pointerEvents = 'auto';
        });

        if (!modal.hasAttribute('tabindex')) {
            modal.setAttribute('tabindex', '-1');
        }
    };

    const corrigirCamadasDoModal = (modal) => {
        if (!modal || !modal.classList.contains('modal')) {
            return;
        }

        prepararInteracaoModal(modal);
        modal.style.setProperty('z-index', '1095', 'important');
        modal.style.pointerEvents = 'auto';

        const dialog = modal.querySelector('.modal-dialog');
        if (dialog) {
            dialog.style.position = 'relative';
            dialog.style.setProperty('z-index', '1096', 'important');
            dialog.style.pointerEvents = 'auto';
        }

        const conteudo = modal.querySelector('.modal-content');
        if (conteudo) {
            conteudo.style.setProperty('z-index', '1097', 'important');
            conteudo.style.pointerEvents = 'auto';
        }

        document.querySelectorAll('.modal-backdrop.show').forEach((backdrop) => {
            backdrop.style.setProperty('z-index', '1085', 'important');
        });

        document.querySelectorAll('.membresia-backdrop').forEach((backdrop) => {
            backdrop.style.setProperty('z-index', '1080', 'important');
        });
    };

    const agendarCorrecaoCamadasDoModal = (modal) => {
        corrigirCamadasDoModal(modal);
        window.setTimeout(() => corrigirCamadasDoModal(modal), 0);
        window.setTimeout(() => corrigirCamadasDoModal(modal), 120);
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
            elemento.classList.remove('is-open');
            elemento.setAttribute('aria-hidden', 'true');
        });

        liberarPagina();
    };

    const abrirOverlay = (alvo) => {
        if (!alvo) {
            return;
        }

        alvo.classList.remove('show');
        alvo.classList.add('is-open');
        alvo.removeAttribute('aria-hidden');
        document.body.classList.add('membresia-overlay-open');
        garantirBackdrop().addEventListener('click', fecharOverlay, { once: true });

        if (alvo.classList.contains('modal')) {
            agendarCorrecaoCamadasDoModal(alvo);
        }

        const campoFoco = alvo.querySelector('input, select, textarea, button:not(.btn-close)');
        if (campoFoco) {
            window.setTimeout(() => campoFoco.focus(), 80);
        }
    };

    document.querySelectorAll('.modal, .offcanvas').forEach((elemento) => {
        elemento.addEventListener('show.bs.modal', () => {
            elemento.classList.remove('is-open');
            removerBackdropLocal();
            agendarCorrecaoCamadasDoModal(elemento);
        });
        elemento.addEventListener('shown.bs.modal', () => agendarCorrecaoCamadasDoModal(elemento));
        elemento.addEventListener('show.bs.offcanvas', () => {
            elemento.classList.remove('is-open');
            removerBackdropLocal();
        });
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

            const temBootstrap = window.bootstrap
                && ((alvo.classList.contains('offcanvas') && window.bootstrap.Offcanvas)
                    || (alvo.classList.contains('modal') && window.bootstrap.Modal));

            if (!temBootstrap) {
                evento.preventDefault();
                abrirOverlay(alvo);
                return;
            }

            evento.preventDefault();
            evento.stopPropagation();
            if (typeof evento.stopImmediatePropagation === 'function') {
                evento.stopImmediatePropagation();
            }

            removerBackdropLocal();
            alvo.classList.remove('is-open');
            alvo.removeAttribute('aria-hidden');

            if (alvo.classList.contains('modal')) {
                document.querySelectorAll('.modal.show').forEach((modalAberto) => {
                    if (modalAberto !== alvo && window.bootstrap.Modal) {
                        const instanciaAberta = window.bootstrap.Modal.getInstance(modalAberto);
                        if (instanciaAberta) {
                            instanciaAberta.hide();
                        }
                    }
                });

                const instancia = window.bootstrap.Modal.getOrCreateInstance(alvo, {
                    backdrop: true,
                    focus: true,
                });
                instancia.show();
                agendarCorrecaoCamadasDoModal(alvo);
                return;
            }

            if (alvo.classList.contains('offcanvas')) {
                const instancia = window.bootstrap.Offcanvas.getOrCreateInstance(alvo, {
                    backdrop: true,
                    scroll: false,
                });
                instancia.show();
            }
        });
    });

    document.addEventListener('submit', (evento) => {
        const formulario = evento.target.closest('form.filter-modal');
        if (!formulario) {
            return;
        }

        const metodo = (formulario.getAttribute('method') || 'get').toLowerCase();
        if (metodo !== 'get') {
            return;
        }

        evento.preventDefault();

        const destino = formulario.getAttribute('action') || window.location.pathname;
        const url = new URL(destino, window.location.origin);
        const dados = new FormData(formulario);
        const parametros = new URLSearchParams();

        dados.forEach((valor, chave) => {
            const texto = String(valor || '').trim();
            if (texto && texto !== 'Todos' && texto !== 'Selecione') {
                parametros.set(chave, texto);
            }
        });

        url.search = parametros.toString();

        const overlayPai = formulario.closest('.modal, .offcanvas');
        if (overlayPai && window.bootstrap) {
            if (overlayPai.classList.contains('modal') && window.bootstrap.Modal) {
                const instancia = window.bootstrap.Modal.getInstance(overlayPai);
                if (instancia) {
                    instancia.hide();
                }
            } else if (overlayPai.classList.contains('offcanvas') && window.bootstrap.Offcanvas) {
                const instancia = window.bootstrap.Offcanvas.getInstance(overlayPai);
                if (instancia) {
                    instancia.hide();
                }
            }
        } else if (overlayPai) {
            fecharOverlay();
        }

        window.setTimeout(() => {
            liberarPagina();
            window.location.assign(url.toString());
        }, 30);
    });

    document.querySelectorAll('form.filter-modal a[href]').forEach((link) => {
        link.addEventListener('click', () => {
            liberarPagina();
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
