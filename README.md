# Sistema de Membresia Church

Sistema web responsivo para gestão de membresia de igreja, construído com Python, Flask, templates HTML, Bootstrap e base planejada para MySQL.

## Visão Geral

O projeto centraliza cadastros e rotinas administrativas da igreja em módulos:

- Dashboard
- Membros
- Visitantes
- Ministérios
- Células e grupos pequenos
- Presença
- Eventos
- Financeiro
- Comunicação
- Relatórios
- Usuários e permissões
- Configurações

Nesta versão, a aplicação Flask funciona como protótipo navegável com dados em memória e as migrações SQL deixam a estrutura MySQL pronta para persistência real.

## Funcionalidades Implementadas no Protótipo

### Acesso

- Login e logout.
- Recuperação de senha por fluxo inicial.
- Cadastro público de usuário.
- Cadastro administrativo de usuários.
- Perfis: Administrador, Pastor, Secretaria, Líder e Financeiro.
- Status de usuário: Ativo, Bloqueado e Inativo.
- Hash de senha com Werkzeug.
- Registro de último acesso em memória.

Usuário inicial para teste:

```text
E-mail: admin@igreja.org
Senha: admin123
```

### Membros e Visitantes

- Cadastro de membros e visitantes.
- Edição de dados pessoais.
- Inativação de membro.
- Exclusão lógica, preservando o registro em memória.
- Busca por nome, telefone, WhatsApp, e-mail, CPF, célula, cargo/função e ministério.
- Filtro por status: Ativo, Inativo, Visitante e Afastado.
- Controle de data de nascimento, endereço, telefone, WhatsApp, e-mail, estado civil, profissão, entrada na igreja, batismo, ministérios, célula e cargo/função.
- Histórico espiritual por pessoa.

### Histórico Espiritual e Pastoral

Registros disponíveis:

- Batismo
- Conversão
- Profissão de fé
- Transferência de igreja
- Desligamento
- Discipulado
- Acompanhamento pastoral
- Pedido de oração
- Testemunho
- Aconselhamento
- Observação espiritual

### Ministérios

- Cadastro, edição, inativação e exclusão lógica.
- Líder, dia de reunião, vagas, status, participantes e atividades.
- Base para relatório por ministério.

### Células, Presença, Eventos, Financeiro e Comunicação

Há telas de resumo para:

- Células e grupos pequenos, com líderes, membros, visitantes e crescimento.
- Presença, com filtro por data e membro.
- Eventos, com inscrições de membros e visitantes.
- Financeiro, com entradas, saídas, dízimos, ofertas, contribuições, categorias e contas.
- Comunicação, com canais WhatsApp, e-mail e notificações internas.

### Relatórios e Administração

O módulo de relatórios mapeia:

- Membros ativos
- Membros inativos
- Visitantes
- Aniversariantes
- Batizados
- Novos membros
- Membros por ministério
- Membros por célula
- Presença
- Financeiro
- Crescimento da igreja

Configurações contempladas:

- Dados da igreja
- Logo
- Cargos e perfis
- Tipos de membro
- Mensagens padrão
- Backups
- Parâmetros gerais

## Estrutura do Projeto

```text
.
├── app.py
├── requirements.txt
├── database
│   ├── migrations
│   │   ├── 0001_core_security.sql
│   │   └── 0002_membresia_core.sql
│   └── seeds
│       └── 0001_rbac_perfis_permissoes.sql
├── static
│   ├── css
│   ├── imgs
│   └── js
├── templates
│   ├── membros
│   ├── ministerios
│   ├── modulos
│   └── usuarios
└── tests
```

## Banco de Dados MySQL

As migrações ficam em `database/migrations`.

Ordem recomendada:

```sql
SOURCE database/migrations/0001_core_security.sql;
SOURCE database/migrations/0002_membresia_core.sql;
SOURCE database/seeds/0001_rbac_perfis_permissoes.sql;
```

Principais tabelas:

- `usuarios`, `perfis`, `permissoes`, `usuario_perfil`, `perfil_permissao`, `usuario_permissao`
- `auditoria_logs`
- `igrejas`
- `membros`
- `ministerios`
- `membro_ministerio`
- `celulas`
- `celula_reunioes`
- `celula_presencas`
- `historico_espiritual`
- `eventos`
- `evento_inscricoes`
- `presencas`
- `categorias_financeiras`
- `contas_financeiras`
- `lancamentos_financeiros`
- `comunicacao_listas`
- `mensagens`
- `mensagem_destinatarios`
- `configuracoes_sistema`

## Como Executar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute a aplicação:

```powershell
flask --app app run --debug
```

Acesse:

```text
http://127.0.0.1:5000
```

## Testes

Execute a suíte com:

```powershell
python -m unittest discover -s tests -q
```

## Requisitos Técnicos Atendidos

- Sistema web responsivo.
- Backend em Python/Flask.
- Templates HTML com Bootstrap.
- Estrutura MySQL planejada.
- Senhas criptografadas no protótipo.
- Validação de formulários.
- Login seguro para fluxo inicial.
- Exclusão lógica nos cadastros principais.
- Busca e filtros.
- Base para auditoria de ações.
- Base para permissões por módulo.
- Base para exportação de relatórios.
- Organização por módulos.

## Próximos Passos Recomendados

- Conectar o Flask ao MySQL com camada de persistência.
- Substituir dados em memória por modelos e repositórios.
- Implementar permissões por rota usando as tabelas RBAC.
- Criar paginação real nas listagens.
- Adicionar exportação PDF/Excel.
- Implementar envio real por WhatsApp/e-mail.
- Implementar backup automatizado do banco.
- Ampliar testes de CRUD, autenticação, permissões e relatórios.
