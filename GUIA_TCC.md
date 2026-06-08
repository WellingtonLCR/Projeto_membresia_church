# 📚 Guia de Organização - TCC Sistema de Membresia

> **Projeto:** Sistema de Membresia da Igreja Viva  
> **Desenvolvedor:** Wellington Luis Costa Ribeiro  
> **Orientador:** Prof. Ronan Adriel Zenatti  
> **Instituição:** FATEC Jahu - Faculdade de Tecnologia de Jahu  
> **Curso:** Tecnologia em Sistemas para Internet  
> **Data:** 2026

---

## 📑 Índice de Entrega

- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Funcionalidades Implementadas](#-funcionalidades-implementadas)
- [Validação das Funções](#-validação-das-funções)
- [Como Executar](#-como-executar)
- [Testes Automatizados](#-testes-automatizados)
- [Arquivos de Documentação](#-arquivos-de-documentação)
- [Checklist de Avaliação](#-checklist-de-avaliação)

---

## 🏗️ Estrutura do Projeto

```
Projeto_membresia_church/
│
├── 📄 app.py                          # Aplicação Flask (2000+ linhas)
├── 📄 db.py                           # Camada de banco de dados
├── 📄 db_setup.py                     # Script de inicialização
├── 📄 requirements.txt                # Dependências Python
├── 📄 README.md                       # Documentação principal
├── 📄 GUIA_TCC.md                     # Este arquivo
│
├── 📁 database/
│   ├── 📁 migrations/                 # Scripts de criação de banco
│   │   ├── 0001_core_security.sql    # Tabelas de segurança (usuários, perfis, permissões)
│   │   └── 0002_membresia_core.sql   # Tabelas de negócio (membros, eventos, financeiro, etc.)
│   │
│   └── 📁 seeds/                      # Dados iniciais
│       ├── 0001_rbac_perfis_permissoes.sql
│       ├── 0002_dados_demo_app.sql
│       └── 0003_dados_historicos_2024_2026.sql
│
├── 📁 templates/
│   ├── base.html                      # Template base (admin)
│   ├── base_publica.html              # Template base (público)
│   ├── login.html                     # Autenticação
│   ├── dashboard.html                 # Painel executivo
│   │
│   ├── 📁 app_usuario/                # Interface do usuário final
│   │   ├── base.html
│   │   ├── inicio.html
│   │   ├── cultos.html
│   │   ├── evento.html
│   │   ├── eventos.html
│   │   ├── doacoes.html
│   │   ├── feed.html
│   │   └── oracao.html
│   │
│   ├── 📁 membros/                    # CRUD de membros
│   ├── 📁 eventos/                    # Gestão de eventos
│   ├── 📁 financeiro/                 # Receitas, despesas, contas
│   ├── 📁 doacoes/                    # Registro de doações
│   ├── 📁 ministerios/                # Ministérios e líderes
│   ├── 📁 celulas/                    # Células e pequenos grupos
│   ├── 📁 comunicacao/                # Comunicados e mensagens
│   ├── 📁 mural/                      # Avisos e feed
│   ├── 📁 intercessao/                # Oração e pedidos
│   ├── 📁 relatorios/                 # Indicadores e métricas
│   ├── 📁 usuarios/                   # Gerenciamento de usuários
│   ├── 📁 configuracoes/              # Configurações do sistema
│   ├── 📁 familias/                   # Gestão de famílias
│   ├── 📁 fornecedores/               # Prestadores de serviço
│   ├── 📁 presencas/                  # Controle de presença
│   └── 📁 partials/                   # Componentes reutilizáveis
│
├── 📁 static/
│   ├── 📁 css/
│   │   └── styles.css                 # Estilos customizados (4900+ linhas)
│   │
│   ├── 📁 js/
│   │   └── script.js                  # JavaScript customizado
│   │
│   └── 📁 imgs/
│       ├── logo_church.png
│       └── ...
│
├── 📁 tests/
│   └── test_membresia_app.py          # Suite de testes automatizados
│
└── 📁 material_TCC/
    ├── 📄 Sistema_Membresia_Igreja_Viva_TCC_ABNT_Final.docx
    └── ... (referências do projeto)
```

---

## ✨ Funcionalidades Implementadas

### ✅ Autenticação e Controle de Acesso
- [x] Login com validação de credenciais
- [x] Controle de perfis (6 tipos: Administrador, Pastor, Secretaria, Líder, Financeiro, Visitante)
- [x] Sessões seguras do Flask
- [x] Hash de senha com Werkzeug
- [x] Proteção de rotas com `@login_required`
- [x] Redirecionamento baseado em perfil

### ✅ Módulo de Pessoas
- [x] Cadastro de membros (nome, CPF, data de nascimento, telefone, email)
- [x] Cadastro de visitantes (com possibilidade de upgrade)
- [x] Gerenciamento de famílias
- [x] Histórico espiritual (Batismo, Conversão, Profissão de fé, etc.)
- [x] Consulta de aniversários do mês
- [x] Filtros por situação (Ativo, Inativo, Visitante, Afastado)
- [x] Busca por múltiplos campos

### ✅ Módulo Financeiro
- [x] Registr de receitas (Entrada)
- [x] Registro de despesas (Saída)
- [x] Múltiplas contas (Caixa, Banco, POV, etc.)
- [x] Categorias financeiras por tipo
- [x] Formas de pagamento/recebimento (PIX, Cartão, Dinheiro, Boleto, etc.)
- [x] Painel de métricas (Total de receitas, despesas, saldo)
- [x] Filtros por período, conta, categoria, usuário
- [x] Dashboard financeiro com gráficos
- [x] Exportação de relatórios

### ✅ Módulo de Eventos e Cultos
- [x] Cadastro de eventos (Cultos, Retiros, Conferências)
- [x] Definição de dias de reunião (seg-dom)
- [x] Status de eventos (Agendado, Realizado, Cancelado)
- [x] Painel público de eventos
- [x] Controle de presença

### ✅ Módulo de Doações
- [x] Registro de doações com tipos (Dízimo, Oferta, Contribuição, Campanha, Missão)
- [x] Status de doações (Recebida, Pendente, Cancelada)
- [x] Associação com membro ou anônimo
- [x] Dashboard de doações
- [x] Painel público para doações online

### ✅ Módulo de Intercessão
- [x] Cadastro de pedidos de oração (público e privado)
- [x] Categorias de oração (Saúde, Família, Trabalho, Vida espiritual)
- [x] Sistema de reações (Estou orando, Amém, Força)
- [x] Comentários aprovados em pedidos públicos
- [x] Status de pedidos (Pendente, Em oração, Respondido, Arquivado)

### ✅ Módulo de Comunicação
- [x] Publicação de avisos (Rascunho, Publicado, Arquivado)
- [x] Devocional diário
- [x] Feed público de notícias
- [x] Sistema de categorias

### ✅ Módulo de Ministérios
- [x] Cadastro de ministérios
- [x] Associação de membros a ministérios
- [x] Controle de líderes
- [x] Status (Ativo/Inativo)
- [x] Número de vagas

### ✅ Módulo de Células
- [x] Cadastro de células (pequenos grupos)
- [x] Associação de membros
- [x] Controle de presença
- [x] Status (Ativo/Inativo)

### ✅ Relatórios e Indicadores
- [x] Dashboard com métricas principais
- [x] Relatório de pessoas (membros, visitantes, famílias)
- [x] Relatório financeiro (receitas, despesas, saldo)
- [x] Relatório de eclesiástico (batizados, novos membros, ministérios)
- [x] Relatório de comunicação (avisos, mensagens, feed)
- [x] Relatório de intercessão (pedidos de oração, respostas)
- [x] Geração de PDF simples

### ✅ App do Usuário (Frente Pública)
- [x] Home com resumo de eventos e avisos
- [x] Calendário de cultos
- [x] Lista de eventos com descrição
- [x] Feed de avisos
- [x] Devocional diário
- [x] Pedidos de oração (enviar + visualizar respostas)
- [x] Doações online
- [x] Cadastro de visitante

### ✅ Segurança e Validações
- [x] SQL parametrizado (injection prevention)
- [x] Validação de CPF
- [x] Validação de e-mail
- [x] Validação de telefone com DDD
- [x] Hash de senha com salt
- [x] Exclusão lógica de dados
- [x] Pool de conexões MySQL

### ✅ Funcionalidades Técnicas
- [x] Herança de templates (base.html, base_publica.html)
- [x] Filtros Jinja2 customizados (data_br, moeda_br, rotulo)
- [x] Context processor para layout
- [x] Flash messages para feedback ao usuário
- [x] Upload de imagens (eventos, mural)
- [x] Responsividade com Bootstrap 5
- [x] Menu lateral colapsável
- [x] Modais sem fade animation (ajuste visual)
- [x] CSS custom com 4900+ linhas
- [x] JavaScript para interatividade

---

## ✔️ Validação das Funções

### Função: `login_required` (Segurança)
```python
# ✅ Valida se usuário está logado
# ✅ Redireciona visitantes para app
# ✅ Protege todas as rotas administrativas
```

### Função: `criar_usuario` (CRUD - Criar)
```python
# ✅ Insere usuário no banco
# ✅ Gera hash de senha
# ✅ Associa perfil ao usuário
# ✅ Retorna ID do usuário criado
```

### Função: `listar_membros_db` (CRUD - Listar)
```python
# ✅ Busca com múltiplos filtros
# ✅ Busca por nome, telefone, email, cpf, etc.
# ✅ Filtro por situação (Ativo, Visitante, etc.)
# ✅ Retorna lista de membros formatada
```

### Função: `inserir_membro_db` (CRUD - Inserir)
```python
# ✅ Insere membro na tabela
# ✅ Valida dados obrigatórios
# ✅ Associa ministérios
# ✅ Salva célula
# ✅ Transaction com rollback em erro
```

### Função: `listar_lancamentos_financeiros` (Filtros)
```python
# ✅ Filtra por tipo (Entrada/Saída)
# ✅ Filtra por período (data_inicio, data_fim)
# ✅ Filtra por conta
# ✅ Filtra por categoria
# ✅ Filtra por usuário
# ✅ Retorna lista formatada com valores
```

### Função: `gerar_metricas` (Dashboard)
```python
# ✅ Calcula total de pessoas
# ✅ Calcula membros por situação
# ✅ Calcula totalizadores financeiros
# ✅ Calcula indicadores de engajamento
# ✅ Retorna dict com todas as métricas
```

### Função: `perfil_eh_visitante` (Controle de Acesso)
```python
# ✅ Verifica se perfil é visitante
# ✅ Normaliza nome de perfil
# ✅ Retorna bool
```

### Função: `validar_email` (Validação)
```python
# ✅ Valida padrão de e-mail
# ✅ Usa regex robusta
# ✅ Retorna bool
```

### Função: `validar_telefone` (Validação)
```python
# ✅ Valida padrão telefônico com DDD
# ✅ Aceita múltiplos formatos (com parênteses, hífen)
# ✅ Retorna bool
```

### Função: `validar_cpf` (Validação)
```python
# ✅ Valida padrão de CPF
# ✅ Aceita CPF com ou sem máscara
# ✅ Retorna bool
```

---

## 🚀 Como Executar

### 1️⃣ Clonar e Preparar Ambiente
```bash
git clone https://github.com/WellingtonLCR/Projeto_membresia_church.git
cd Projeto_membresia_church
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2️⃣ Configurar Banco de Dados
```bash
# Variáveis de ambiente
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=sua_senha
export MYSQL_DATABASE=membresia_church
export SECRET_KEY=sua_chave_secreta_longa_e_aleatoria
```

### 3️⃣ Inicializar Banco de Dados
```bash
python db_setup.py
# Isso executará:
# - database/migrations/0001_core_security.sql
# - database/migrations/0002_membresia_core.sql
# - database/seeds/0001_rbac_perfis_permissoes.sql
# - database/seeds/0002_dados_demo_app.sql
# - database/seeds/0003_dados_historicos_2024_2026.sql
```

### 4️⃣ Executar a Aplicação
```bash
python app.py
# Acesse: http://127.0.0.1:5000
```

### 5️⃣ Fazer Login
- **Email:** admin@igreja.org
- **Senha:** senha123

---

## 🧪 Testes Automatizados

### Executar Testes
```bash
python -m unittest discover tests/
# ou
python -m pytest tests/
```

### Testes Implementados
```python
# ✅ test_rotas_publicas_renderizam
# ✅ test_assets_essenciais_sao_entregues
# ✅ test_login_com_credenciais_corretas
# ✅ test_login_com_credenciais_incorretas
# ✅ test_rotas_administrativas_bloqueadas_sem_login
# ✅ test_visitante_redirecionado_do_admin
# ✅ test_cadastro_publico_cria_visitante
# ✅ test_app_usuario_exibe_dados_admin
```

---

## 📄 Arquivos de Documentação

### Principais Arquivos
| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação completa do projeto |
| `GUIA_TCC.md` | Este guia de organização |
| `app.py` | Código-fonte principal (2000+ linhas) |
| `db.py` | Camada de banco de dados |
| `requirements.txt` | Dependências Python |

### Scripts SQL
| Script | Descrição |
|--------|-----------|
| `database/migrations/0001_core_security.sql` | Tabelas de autenticação e RBAC |
| `database/migrations/0002_membresia_core.sql` | Tabelas de negócio |
| `database/seeds/0001_rbac_perfis_permissoes.sql` | Perfis e permissões iniciais |
| `database/seeds/0002_dados_demo_app.sql` | Dados demonstrativos |
| `database/seeds/0003_dados_historicos_2024_2026.sql` | Dados históricos para testes |

### Templates
| Template | Descrição |
|----------|-----------|
| `base.html` | Layout administrativo |
| `base_publica.html` | Layout público |
| `app_usuario/base.html` | Layout do app do usuário |

### Estáticos
| Arquivo | Descrição |
|---------|-----------|
| `static/css/styles.css` | Estilos customizados (4900+ linhas) |
| `static/js/script.js` | JavaScript customizado |

---

## ✅ Checklist de Avaliação

### Requisitos Funcionais
- [x] Login com segurança (hash de senha)
- [x] Controle de perfis (6 tipos diferentes)
- [x] Cadastro de membros com validações
- [x] Cadastro de eventos e cultos
- [x] Controle financeiro (receitas/despesas)
- [x] Sistema de doações
- [x] Pedidos de oração com respostas
- [x] Feed e avisos públicos
- [x] Relatórios e métricas
- [x] Exclusão lógica de dados

### Requisitos Não-Funcionais
- [x] Responsividade (Bootstrap 5)
- [x] Segurança (SQL parametrizado, hash de senha)
- [x] Performance (pool de conexões)
- [x] Usabilidade (UI intuitiva, feedback visual)
- [x] Manutenibilidade (código organizado, comentado)
- [x] Escalabilidade (arquitetura modular)

### Padrões de Desenvolvimento
- [x] Padrão MVC (Model-View-Controller)
- [x] Separação de responsabilidades
- [x] DRY (Don't Repeat Yourself)
- [x] CRUD completo para principais entidades
- [x] Transactions para operações críticas
- [x] Herança de templates

### Testes
- [x] Testes automatizados implementados
- [x] Cobertura de rotas principais
- [x] Validação de segurança
- [x] Teste de funcionalidades críticas

---

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| Arquivos Python | 3 |
| Linhas de código (app.py) | 2000+ |
| Linhas de CSS | 4900+ |
| Templates HTML | 40+ |
| Tabelas no banco | 25+ |
| Rotas implementadas | 60+ |
| Perfis de usuário | 6 |
| Validações | 10+ |
| Testes automatizados | 8+ |
| Funcionalidades principais | 13 |

---

## 🎯 Objetivos Acadêmicos Atendidos

✅ **Objetivo Geral:** Desenvolver um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e MySQL  
✅ **Objetivo Específico 1:** Criar aplicação Flask com rotas públicas e rotas protegidas por login  
✅ **Objetivo Específico 2:** Utilizar templates Jinja2 com herança  
✅ **Objetivo Específico 3:** Implementar formulários com validação no back-end  
✅ **Objetivo Específico 4:** Persistir dados principais em banco MySQL real  
✅ **Objetivo Específico 5:** Criar operações CRUD (cadastro, listagem, edição, exclusão lógica)  
✅ **Objetivo Específico 6:** Organizar templates por entidade  
✅ **Objetivo Específico 7:** Desenvolver interface responsiva com Bootstrap e CSS próprio  
✅ **Objetivo Específico 8:** Implementar relatórios com opções de exportação e impressão  
✅ **Objetivo Específico 9:** Registrar testes automatizados  

---

## 📞 Informações de Contato

**Desenvolvedor:** Wellington Luis Costa Ribeiro  
**GitHub:** [https://github.com/WellingtonLCR](https://github.com/WellingtonLCR)  
**Repositório:** [Projeto_membresia_church](https://github.com/WellingtonLCR/Projeto_membresia_church)  
**Orientador:** Prof. Ronan Adriel Zenatti  
**Instituição:** FATEC Jahu  

---

## 📝 Notas Finais

Este sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do programa de Tecnologia em Sistemas para Internet da FATEC Jahu. O projeto incorpora conceitos de programação web, banco de dados relacional, segurança de aplicações e usabilidade.

**Validação Final:** ✅ **100% Concluído e Testado**

Data de conclusão: **07/06/2026**
