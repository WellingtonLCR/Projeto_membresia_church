# Sistema de Membresia da Igreja Viva

> **TCC - Tecnologia em Sistemas para Internet**  
> FATEC Jahu | Prof. Ronan Adriel Zenatti | 2026

## 📋 Sobre o Projeto

Sistema web completo para gerenciamento administrativo de igrejas, centraliza cadastros, controles e processos que normalmente ficam espalhados em planilhas e registros informais.

**Desenvolvido com:** Python, Flask, Jinja2, Bootstrap, MySQL

---

## ✨ Funcionalidades Principais

### 🔐 Autenticação e Controle de Acesso
- ✅ Login seguro com hash de senha (Werkzeug)
- ✅ Controle de perfis (Administrador, Pastor, Secretaria, Líder, Financeiro, Visitante)
- ✅ Rotas protegidas com decorador `@login_required`
- ✅ Sessões de usuário gerenciadas pelo Flask
- ✅ Cadastro público para visitantes

### 👥 Módulo de Pessoas
- ✅ Cadastro de membros e visitantes
- ✅ Gerenciamento de famílias
- ✅ Histórico espiritual (Batismo, Conversão, Profissão de fé, etc.)
- ✅ Consulta de aniversários
- ✅ Filtros e busca avançada

### 📊 Módulo Financeiro
- ✅ Gestão de receitas e despesas
- ✅ Controle de categorias (Dízimo, Oferta, Contribuição, etc.)
- ✅ Múltiplas contas (Caixa, Banco, POV, etc.)
- ✅ Formas de pagamento/recebimento
- ✅ Dashboard com métricas financeiras
- ✅ Relatórios de fluxo de caixa

### ⛪ Módulo de Eventos e Cultos
- ✅ Cadastro de eventos (Cultos, Retiros, Conferências)
- ✅ Gerenciamento de presença
- ✅ Dias da semana de reuniões
- ✅ Status de eventos (Agendado, Realizado, Cancelado)

### 🙏 Módulo de Intercessão
- ✅ Pedidos de oração públicos e privados
- ✅ Sistema de reações (Estou orando, Amém, Força)
- ✅ Comentários em pedidos
- ✅ Categorias de oração (Saúde, Família, Trabalho, etc.)

### 📢 Comunicação e Mural
- ✅ Publicação de avisos (Rascunho, Publicado, Arquivado)
- ✅ Devocional diário
- ✅ Feed público de notícias
- ✅ Sistema de categorias

### 💰 Doações
- ✅ Registro de doações (Recebida, Pendente, Cancelada)
- ✅ Tipos de doação e campanhas
- ✅ Rastreamento de doantes

### 📋 Relatórios e Exportação
- ✅ Relatórios financeiros
- ✅ Exportação para Excel
- ✅ Impressão de documentos
- ✅ Gráficos de análise

---

## 🏗️ Arquitetura

```
Projeto_membresia_church/
├── app.py                 # Aplicação Flask (rotas, validações)
├── db.py                  # Camada de banco de dados
├── db_setup.py            # Script de inicialização do banco
├── requirements.txt       # Dependências Python
│
├── database/
│   ├── migrations/        # Scripts SQL (criação de tabelas)
│   │   ├── 0001_core_security.sql
│   │   └── 0002_membresia_core.sql
│   └── seeds/             # Dados iniciais (RBAC, demo)
│       ├── 0001_rbac_perfis_permissoes.sql
│       ├── 0002_dados_demo_app.sql
│       └── 0003_dados_historicos_2024_2026.sql
│
├── templates/             # Templates Jinja2
│   ├── base.html          # Template base admin
│   ├── base_publica.html  # Template base público
│   ├── dashboard.html
│   ├── login.html
│   ├── membros/
│   ├── eventos/
│   ├── financeiro/
│   ├── doacoes/
│   ├── comunicacao/
│   ├── app_usuario/       # Interface do usuário final
│   └── ...
│
├── static/
│   ├── css/
│   │   └── styles.css     # Estilos customizados (4900+ linhas)
│   ├── js/
│   │   └── script.js      # JavaScript customizado
│   └── imgs/              # Imagens do sistema
│
├── tests/
│   └── test_membresia_app.py  # Testes automatizados
│
└── README.md              # Este arquivo
```

---

## 🚀 Configuração e Instalação

### Pré-requisitos
- Python 3.8+
- MySQL 5.7+
- Git

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/WellingtonLCR/Projeto_membresia_church.git
cd Projeto_membresia_church
```

### Passo 2: Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados
```bash
# Editar variáveis de ambiente (ou criar .env)
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=sua_senha
export MYSQL_DATABASE=membresia_church
export SECRET_KEY=sua_chave_secreta

# Windows
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=sua_senha
```

### Passo 5: Inicializar Banco de Dados
```bash
python db_setup.py
```

### Passo 6: Executar a Aplicação
```bash
python app.py
```

Acesse: **http://127.0.0.1:5000**

---

## 👤 Usuários Padrão

Após executar `db_setup.py`, use:

| Tipo | Email | Senha | Perfil |
|------|-------|-------|--------|
| Admin | admin@igreja.org | senha123 | Administrador |
| Visitante | visitante@igreja.org | senha123 | Visitante |

---

## 📂 Principais Rotas

### Públicas
| Rota | Descrição |
|------|-----------|
| `/` | Página inicial |
| `/login` | Autenticação |
| `/cadastro` | Registro de visitantes |
| `/sobre-equipe` | Informações da equipe |
| `/app` | Dashboard do usuário |
| `/app/eventos` | Lista de eventos |
| `/app/cultos` | Cultos e reuniões |
| `/app/feed` | Feed de notícias |
| `/app/devocional` | Devocional diário |
| `/app/oracao` | Pedidos de oração |
| `/app/doacoes` | Doações |

### Administrativas
| Rota | Descrição |
|------|-----------|
| `/dashboard` | Painel executivo |
| `/membros/listar` | Lista de membros |
| `/usuarios/listar` | Gerenciamento de usuários |
| `/financeiro/receitas` | Receitas |
| `/financeiro/despesas` | Despesas |
| `/eventos/listar` | Gerenciamento de eventos |
| `/ministerios/listar` | Lista de ministérios |
| `/doacoes/listar` | Doações recebidas |
| `/relatorios/listar` | Relatórios diversos |

---

## 🗄️ Modelo de Dados

### Principais Entidades
- **usuarios**: Conta de acesso
- **membros**: Pessoas (membros, visitantes, afastados)
- **familias**: Agrupamento de membros
- **ministerios**: Áreas de serviço
- **celulas**: Pequenos grupos
- **eventos**: Reuniões e atividades
- **presencas**: Registro de comparecimento
- **lancamentos_financeiros**: Receitas e despesas
- **contas**: Caixas e bancos
- **categorias_financeiras**: Tipos de movimento
- **doacoes**: Contribuições de membros
- **mural**: Avisos e notícias
- **pedidos_oracao**: Oração de membros
- **fornecedores**: Prestadores de serviço

---

## 🔒 Segurança

✅ **Implementado:**
- Hash de senha com Werkzeug
- Queries parametrizadas (SQL injection prevention)
- Exclusão lógica de dados
- Controle de acesso por perfil
- Sessões seguras do Flask
- Validação de formulários no back-end

---

## 🧪 Testes

Executar testes:
```bash
python -m pytest tests/
# ou
python -m unittest discover tests/
```

Os testes cobrem:
- ✅ Renderização de rotas públicas
- ✅ Bloqueio de rotas protegidas sem autenticação
- ✅ Validação de formulários
- ✅ Operações CRUD
- ✅ Redirecionamentos após ações

---

## 📊 Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| Flask | 3.1.3 | Framework web |
| Jinja2 | 3.1.6 | Motor de templates |
| Werkzeug | 3.1.7 | Utilitários web |
| mysql-connector-python | 9.5.0 | Driver MySQL |
| Click | 8.3.1 | CLI |
| Blinker | 1.9.0 | Event dispatcher |

Ver `requirements.txt` para lista completa.

---

## 🎨 Customizações CSS

O arquivo `static/css/styles.css` contém:
- Layout responsivo (mobile-first)
- Sistema de cores (primary: #2454e8, teal: #008c7a, orange: #ff6b2c)
- Menu lateral colapsável
- Dashboard com cards
- Tabelas administrativas
- Modais de filtro (sem fade animation)
- Backdrop com tint azul
- Z-index strategy (backdrop: 1040, modal: 1095)

---

## 🌐 API Endpoints

O sistema não expõe uma API REST pública separada. A comunicação ocorre via:
- **GET**: Renderização de páginas
- **POST**: Envio de formulários
- Responses em HTML (Jinja2)
- Redirecionamentos com Flash messages

---

## 📝 Convenções de Código

### Rotas
```python
@app.route("/caminho/<tipo>/<id>", methods=["GET", "POST"])
@login_required
def nome_funcao():
    ...
```

### Funções de Banco
```python
def listar_algo_db(filtros=""):
    sql = "SELECT * FROM tabela WHERE ..."
    return execute_query(sql, params)
```

### Templates
- `templates/entidade/listar_entidade.html`
- `templates/entidade/inserir_entidade.html`
- Herança: `{% extends "base.html" %}`

---

## 🐛 Troubleshooting

### Erro de conexão MySQL
```
Error: Failed to connect to MySQL
```
**Solução:** Verificar variáveis de ambiente e credenciais no banco

### Erro de imports
```
ModuleNotFoundError: No module named 'flask'
```
**Solução:** Executar `pip install -r requirements.txt`

### Templates não encontrados
```
jinja2.exceptions.TemplateNotFound
```
**Solução:** Verificar caminho do arquivo em `templates/`

---

## 📚 Referências e Benchmarking

O projeto foi desenvolvido com base em:
- Material de aulas de Programação para Internet (FATEC Jahu)
- Boas práticas Flask e Jinja2
- Padrões de organização de projetos
- Convenções MySQL e SQL parametrizado

Sistemas analisados como referência:
- ERPNext
- Odoo
- Church Management Systems

---

## 👨‍💻 Autor

**Wellington Luis Costa Ribeiro**  
- GitHub: [@WellingtonLCR](https://github.com/WellingtonLCR)
- Email: wellington.lcr@fatec.sp.gov.br

Desenvolvido para TCC em 2026 sob orientação do Prof. Ronan Adriel Zenatti

---

## 📄 Licença

Projeto acadêmico - FATEC Jahu

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação do TCC em `material_TCC/`
2. Consulte os testes em `tests/`
3. Abra uma issue no GitHub

---

## ✅ Status do Projeto

| Etapa | Status |
|-------|--------|
| Análise | ✅ Concluída |
| Design | ✅ Concluída |
| Desenvolvimento | ✅ Concluída |
| Testes | ✅ Concluída |
| Documentação | ✅ Concluída |
| **Finalizado** | **✅ 100%** |

---

**Última atualização:** 07/06/2026

CENTRO PAULA SOUZA
FACULDADE DE TECNOLOGIA DE JAHU
CURSO DE TECNOLOGIA EM SISTEMAS PARA INTERNET

Wellington Luis Costa Ribeiro

Sistema de Membresia da Igreja Viva

JaÃº, SP
2026

## AGRADECIMENTOS

Agradecemos a Faculdade de Tecnologia de Jahu pela estrutura acadÃªmica e pelo ambiente de aprendizado oferecido durante o desenvolvimento deste projeto.

AgradeÃ§o ao Prof. Ronan Adriel Zenatti, orientador deste projeto, pelo material de aula, pelas orientaÃ§Ãµes sobre Flask, Jinja2, MySQL, CRUD, templates, rotas e organizaÃ§Ã£o de projeto, que serviram como base para a construÃ§Ã£o deste sistema.

AgradeÃ§o tambÃ©m aos colegas de curso pelas trocas de conhecimento, revisÃµes e sugestÃµes feitas durante a evoluÃ§Ã£o da aplicaÃ§Ã£o.

## RESUMO

O presente projeto tem como objetivo o desenvolvimento de um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e banco de dados MySQL. A aplicaÃ§Ã£o foi criada para centralizar cadastros e processos administrativos que normalmente ficam espalhados em planilhas, controles manuais ou registros informais, dificultando a organizaÃ§Ã£o e a consulta das informaÃ§Ãµes.

O sistema permite o gerenciamento de membros, visitantes, famÃ­lias, ministÃ©rios, cÃ©lulas, presenÃ§as, eventos, financeiro, fornecedores, doaÃ§Ãµes, comunicaÃ§Ã£o, mural, pedidos de oraÃ§Ã£o, relatÃ³rios, usuÃ¡rios e configuraÃ§Ãµes. A persistÃªncia dos dados Ã© realizada em banco MySQL real, conforme o conteÃºdo trabalhado nas aulas, sem uso de listas em memÃ³ria para os dados principais do projeto.

Durante o desenvolvimento foram aplicados conceitos de rotas pÃºblicas e privadas, formulÃ¡rios com mÃ©todos GET e POST, heranÃ§a de templates, mensagens de retorno com flash, SQL parametrizado, exclusÃ£o lÃ³gica, validaÃ§Ãµes de formulÃ¡rio e organizaÃ§Ã£o por templates de entidade. O resultado Ã© uma aplicaÃ§Ã£o funcional, estruturada e alinhada aos requisitos acadÃªmicos da disciplina.

Palavras-chave: Flask, MySQL, membresia, igreja, CRUD, sistema web.

## ABSTRACT

This project aims to develop a web-based church membership management system using Python, Flask, Jinja2, Bootstrap, and MySQL. The application centralizes administrative records and processes that are commonly handled through spreadsheets, manual controls, or informal records, making information management and consultation more difficult.

The system supports the management of members, visitors, families, ministries, small groups, attendance, events, finances, suppliers, donations, communication, announcements, prayer requests, reports, users, and system settings. Data persistence is handled through a real MySQL database, following the course material, without using in-memory lists for the main project data.

The development process applied concepts such as public and protected routes, GET and POST forms, template inheritance, flash messages, parameterized SQL queries, logical deletion, form validation, and entity-based template organization. The result is a functional and organized web application aligned with the academic requirements of the course.

Keywords: Flask, MySQL, membership, church, CRUD, web system.

## LISTA DE FIGURAS

Figura 1. Modelo Canvas do Sistema de Membresia da Igreja Viva.
Figura 2. Modelo de casos de uso do sistema.
Figura 3. Modelo conceitual do banco de dados.
Figura 4. PÃ¡gina inicial do sistema.
Figura 5. PÃ¡gina de login.
Figura 6. Dashboard administrativo.
Figura 7. PÃ¡gina de membros.
Figura 8. PÃ¡gina de ministÃ©rios.
Figura 9. PÃ¡gina de cÃ©lulas.
Figura 10. PÃ¡gina de eventos.
Figura 11. PÃ¡gina financeira.
Figura 12. PÃ¡gina de comunicaÃ§Ã£o.
Figura 13. PÃ¡gina de relatÃ³rios.
Figura 14. PÃ¡gina de configuraÃ§Ãµes.
Figura 15. PÃ¡gina da equipe.

## SUMÃRIO

1. INTRODUÃ‡ÃƒO ............................................................. 6
1.1 PROBLEMATIZAÃ‡ÃƒO ...................................................... 6
1.2 Objetivo geral ....................................................... 7
1.3 Objetivos especÃ­ficos ................................................ 7
1.4 METODOLOGIA DA PESQUISA .............................................. 8
1.5 ESTRUTURA DO TRABALHO ................................................ 9
2. REVISÃƒO BIBLIOGRÃFICA ................................................ 10
2.1 SISTEMAS WEB PARA GESTÃƒO ADMINISTRATIVA ............................. 10
2.2 ARQUITETURA E INFRAESTRUTURA DA APLICAÃ‡ÃƒO ........................... 11
2.3 FRONT-END: HTML, CSS, BOOTSTRAP, JINJA2 E JAVASCRIPT ................ 13
2.4 BACK-END: PYTHON E FLASK ............................................ 14
2.5 ROTAS HTTP E API DA APLICAÃ‡ÃƒO ....................................... 15
2.6 PERSISTÃŠNCIA DE DADOS COM MYSQL ..................................... 16
2.7 SEGURANÃ‡A, VALIDAÃ‡ÃƒO E ORGANIZAÃ‡ÃƒO DOS DADOS ....................... 17
2.8 TESTES E FERRAMENTAS DE DESENVOLVIMENTO ............................ 18
2.9 USABILIDADE E ORGANIZAÃ‡ÃƒO DA INFORMAÃ‡ÃƒO ............................ 19
2.10 VIBE CODING NO DESENVOLVIMENTO DO PROJETO ......................... 20
3. MODELO DE NEGÃ“CIOS ................................................... 21
3.1 CANVAS .............................................................. 21
3.2 O QUE SERÃ ELABORADO ................................................ 22
3.3 PARA QUEM SERÃ ELABORADO ........................................... 22
3.4 COMO SERÃ ELABORADO ................................................. 23
3.5 QUANTO CUSTARÃ ...................................................... 23
4. DOCUMENTAÃ‡ÃƒO .......................................................... 24
4.1 DECLARAÃ‡ÃƒO DE ABRANGÃŠNCIA DO PROJETO ............................... 24
4.2 Requisitos funcionais ............................................... 25
4.3 Requisitos nÃ£o funcionais ........................................... 27
4.4 Casos de uso ........................................................ 28
4.5 Modelo conceitual ................................................... 29
4.6 Benchmarking e melhorias identificadas .............................. 30
4.7 Alinhamento com o plano de estudos da disciplina .................... 31
5. MANUAL DO USUÃRIO .................................................... 32
6. CONSIDERAÃ‡Ã•ES FINAIS ................................................. 40
REFERÃŠNCIAS .............................................................. 42

## 1. INTRODUÃ‡ÃƒO

Igrejas e organizaÃ§Ãµes religiosas lidam diariamente com informaÃ§Ãµes de membros, visitantes, ministÃ©rios, cÃ©lulas, eventos, contribuiÃ§Ãµes financeiras, presenÃ§as e comunicaÃ§Ãµes internas. Quando esses dados sÃ£o controlados de forma manual ou descentralizada, a gestÃ£o se torna mais lenta, sujeita a erros e difÃ­cil de acompanhar.

O Sistema de Membresia da Igreja Viva foi desenvolvido como uma aplicaÃ§Ã£o web para auxiliar a administraÃ§Ã£o de uma igreja local. A proposta Ã© reunir em uma Ãºnica plataforma os principais cadastros e controles necessÃ¡rios para a secretaria, lideranÃ§a, ministÃ©rios e equipe administrativa.

O projeto utiliza Flask como framework web, Jinja2 para templates HTML, Bootstrap para interface responsiva e MySQL para armazenamento permanente dos dados. A aplicaÃ§Ã£o segue os padrÃµes trabalhados nas aulas de ProgramaÃ§Ã£o para Internet, especialmente a organizaÃ§Ã£o de rotas, templates, formulÃ¡rios, conexÃ£o com banco de dados e operaÃ§Ãµes CRUD.

### 1.1 PROBLEMATIZAÃ‡ÃƒO

O controle de membresia pode se tornar complexo quando a igreja cresce e passa a lidar com grande volume de informaÃ§Ãµes. Cadastros duplicados, ausÃªncia de histÃ³rico, dificuldade para localizar dados, falta de controle de presenÃ§a, registros financeiros separados e comunicaÃ§Ã£o desorganizada sÃ£o problemas comuns.

Diante desse contexto, surge a seguinte questÃ£o: como desenvolver um sistema web simples, organizado e funcional que permita centralizar os principais processos administrativos de uma igreja, respeitando os conteÃºdos e requisitos da disciplina?

### 1.2 Objetivo geral

Desenvolver um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e MySQL, com funcionalidades de cadastro, consulta, organizaÃ§Ã£o administrativa e relatÃ³rios.

### 1.3 Objetivos especÃ­ficos

- Criar uma aplicaÃ§Ã£o Flask com rotas pÃºblicas e rotas protegidas por login.
- Utilizar templates Jinja2 com heranÃ§a por `base.html` e `base_publica.html`.
- Implementar formulÃ¡rios com validaÃ§Ã£o no back-end.
- Persistir os dados principais em banco MySQL real.
- Criar operaÃ§Ãµes de cadastro, listagem, ediÃ§Ã£o, exclusÃ£o lÃ³gica e aÃ§Ãµes administrativas.
- Organizar os templates por entidade, conforme a estrutura ensinada nas aulas.
- Desenvolver uma interface responsiva com Bootstrap e CSS prÃ³prio.
- Implementar relatÃ³rios com opÃ§Ãµes de exportaÃ§Ã£o e impressÃ£o.
- Registrar testes automatizados para validar rotas e comportamentos principais.

### 1.4 METODOLOGIA DA PESQUISA

O desenvolvimento foi conduzido a partir da anÃ¡lise do material de aula da disciplina de ProgramaÃ§Ã£o para Internet, com foco nas aulas de Flask, Jinja2, formulÃ¡rios, conexÃ£o MySQL, CRUD, autenticaÃ§Ã£o, relatÃ³rios e organizaÃ§Ã£o de projeto.

Inicialmente, foi definida a estrutura base do sistema, contendo `app.py`, `db.py`, `db_setup.py`, `templates`, `static`, `database` e `tests`. Em seguida, foram modeladas as tabelas principais no MySQL, com scripts de migraÃ§Ã£o e seed para dados iniciais.

As funcionalidades foram implementadas por mÃ³dulos, seguindo o fluxo:

- levantamento do caso de uso;
- criaÃ§Ã£o ou ajuste da tabela no banco;
- criaÃ§Ã£o da rota Flask;
- criaÃ§Ã£o do template Jinja2;
- validaÃ§Ã£o dos dados recebidos por formulÃ¡rio;
- persistÃªncia no MySQL com SQL parametrizado;
- teste de renderizaÃ§Ã£o e comportamento.

TambÃ©m foram analisados materiais tÃ©cnicos internos e protÃ³tipos de referÃªncia para identificar funcionalidades que poderiam ser trazidas ao sistema sem fugir do escopo acadÃªmico e sem alterar a arquitetura Flask do projeto.

### 1.5 ESTRUTURA DO TRABALHO

Foi organizado seguindo a estrutura do documento de referÃªncia:

- O CapÃ­tulo 1 apresenta a introduÃ§Ã£o, problema, objetivos e metodologia.
- O CapÃ­tulo 2 apresenta a revisÃ£o bibliogrÃ¡fica relacionada ao projeto.
- O CapÃ­tulo 3 descreve o modelo de negÃ³cios.
- O CapÃ­tulo 4 apresenta a documentaÃ§Ã£o tÃ©cnica e os requisitos.
- O CapÃ­tulo 5 apresenta o manual do usuÃ¡rio.
- O CapÃ­tulo 6 apresenta as consideraÃ§Ãµes finais.

## 2. REVISÃƒO BIBLIOGRÃFICA

### 2.1 SISTEMAS WEB PARA GESTÃƒO ADMINISTRATIVA

Sistemas web permitem que informaÃ§Ãµes sejam acessadas por meio de navegador, sem necessidade de instalaÃ§Ã£o local em cada computador. Em contextos administrativos, esse modelo facilita o registro, consulta e atualizaÃ§Ã£o de dados, alÃ©m de favorecer a padronizaÃ§Ã£o dos processos.

No caso de uma igreja, um sistema web pode apoiar a secretaria e a lideranÃ§a no acompanhamento de membros, visitantes, ministÃ©rios, cÃ©lulas, eventos e presenÃ§as. A centralizaÃ§Ã£o dessas informaÃ§Ãµes reduz retrabalho e melhora a confiabilidade dos dados.

### 2.2 ARQUITETURA E INFRAESTRUTURA DA APLICAÃ‡ÃƒO

A infraestrutura do Sistema de Membresia da Igreja Viva foi organizada como uma aplicaÃ§Ã£o web monolÃ­tica, executada em ambiente local de desenvolvimento. O termo monolÃ­tico, neste contexto, indica que a interface, as regras de negÃ³cio, as rotas HTTP e o acesso ao banco de dados estÃ£o concentrados no mesmo projeto Flask, sem divisÃ£o em serviÃ§os independentes.

O fluxo principal da aplicaÃ§Ã£o pode ser representado da seguinte forma:

```text
Administracao no navegador              Usuario final no navegador
        |                                      |
        | GET/POST em rotas privadas           | GET/POST em rotas publicas do app
        v                                      v
Painel administrativo Flask              App web do usuÃ¡rio Flask
        |                                      |
        | templates/base.html                  | templates/app_usuario/base.html
        |                                      |
        +--------------- app.py ---------------+
                        |
                        | consultas e gravaÃ§Ãµes SQL parametrizadas
                        v
             Camada db.py com mysql-connector-python
                        |
                        v
                  Banco de dados MySQL
```

Nessa estrutura, o navegador acessa pÃ¡ginas do sistema, como login, dashboard, membros, ministÃ©rios, cÃ©lulas, eventos, financeiro e relatÃ³rios. AlÃ©m da frente administrativa, foi criada uma frente pÃºblica em formato de app web para o usuÃ¡rio final, com rotas como `/app`, `/app/eventos`, `/app/cultos`, `/app/feed`, `/app/devocional`, `/app/oracao` e `/app/doacoes`.

O funcionamento segue a lÃ³gica observada nos sistemas estudados no benchmarking: o administrador alimenta informaÃ§Ãµes no painel, e o usuÃ¡rio visualiza uma experiÃªncia mais simples no app. Eventos cadastrados no admin aparecem na agenda pÃºblica, avisos publicados no mural aparecem no feed, publicaÃ§Ãµes de devocional aparecem em uma aba prÃ³pria, configuraÃ§Ãµes de programaÃ§Ã£o e doaÃ§Ãµes aparecem nas telas de cultos e contribuiÃ§Ãµes, e pedidos enviados pelo app entram na tabela de intercessÃ£o para acompanhamento administrativo.

O Flask recebe a requisiÃ§Ã£o, executa as regras necessÃ¡rias, consulta ou grava dados no MySQL e devolve uma pÃ¡gina HTML renderizada pelo Jinja2. Os arquivos estÃ¡ticos ficam separados na pasta `static`, enquanto as telas ficam organizadas na pasta `templates`.

A estrutura fÃ­sica do projeto reforÃ§a essa separaÃ§Ã£o:

- `app.py`: arquivo principal da aplicaÃ§Ã£o, contendo rotas, validaÃ§Ãµes, autenticaÃ§Ã£o e regras dos mÃ³dulos.
- `db.py`: camada de conexÃ£o com o banco MySQL, com pool de conexÃµes e funÃ§Ãµes auxiliares para consultas.
- `db_setup.py`: script de criaÃ§Ã£o e configuraÃ§Ã£o inicial do banco.
- `database/migrations`: scripts SQL responsÃ¡veis pelas tabelas do sistema.
- `database/seeds`: scripts SQL com perfis, permissÃµes, dados iniciais e dados demonstrativos do fluxo admin/app.
- `templates`: pÃ¡ginas HTML renderizadas pelo Flask com Jinja2, incluindo a Ã¡rea administrativa e o app do usuÃ¡rio.
- `static/css`, `static/js` e `static/imgs`: arquivos de estilo, scripts do navegador e imagens.
- `tests`: testes automatizados da aplicaÃ§Ã£o.

Essa organizaÃ§Ã£o foi escolhida por ser simples de compreender, adequada ao escopo acadÃªmico e alinhada ao conteÃºdo trabalhado na disciplina de ProgramaÃ§Ã£o para Internet.

### 2.3 FRONT-END: HTML, CSS, BOOTSTRAP, JINJA2 E JAVASCRIPT

O front-end corresponde Ã  parte visual e interativa acessada pelo usuÃ¡rio no navegador. No projeto, ele foi construÃ­do com HTML, CSS, Bootstrap, Jinja2 e JavaScript.

O HTML define a estrutura das telas, como formulÃ¡rios, tabelas, menus, botÃµes e cards de mÃ©tricas. O CSS prÃ³prio, localizado em `static/css/styles.css`, complementa o Bootstrap e define identidade visual, cores, espaÃ§amentos, menu lateral, dashboard, tabelas, responsividade e o layout mobile-first do app do usuÃ¡rio. O Bootstrap 5.3.3 foi utilizado por meio de CDN para acelerar a criaÃ§Ã£o de uma interface responsiva, com grid, botÃµes, formulÃ¡rios, alertas, cards, offcanvas e componentes visuais prontos.

O Jinja2 funciona como motor de templates. Ele permite reutilizar estruturas comuns, como `base.html`, `base_publica.html` e `templates/app_usuario/base.html`, e preencher cada pÃ¡gina com dados vindos do back-end. Com isso, telas diferentes conseguem compartilhar menu, cabeÃ§alho, rodapÃ©, mensagens de retorno e padrÃ£o visual, reduzindo repetiÃ§Ã£o de cÃ³digo.

O JavaScript do projeto, localizado em `static/js/script.js`, foi usado de forma pontual para melhorar a experiÃªncia do usuÃ¡rio. Entre os recursos implementados estÃ£o a confirmaÃ§Ã£o antes de excluir registros e a indicaÃ§Ã£o de forÃ§a de senha durante o cadastro. A aplicaÃ§Ã£o nÃ£o depende de um framework front-end separado, como React, Vue ou Angular, pois a renderizaÃ§Ã£o principal acontece no servidor Flask.

### 2.4 BACK-END: PYTHON E FLASK

O back-end Ã© a camada responsÃ¡vel por processar as regras do sistema. Neste projeto, ele foi desenvolvido em Python, utilizando o framework Flask. O Python foi escolhido por sua sintaxe simples, boa legibilidade e forte uso em aplicaÃ§Ãµes web, automaÃ§Ã£o, testes e integraÃ§Ã£o com bancos de dados.

O Flask foi utilizado para criar as rotas da aplicaÃ§Ã£o, receber requisiÃ§Ãµes HTTP, controlar sessÃµes de usuÃ¡rio, validar formulÃ¡rios, renderizar templates e redirecionar o usuÃ¡rio apÃ³s cada operaÃ§Ã£o. O arquivo `app.py` concentra as rotas principais, como `/login`, `/dashboard`, `/membros/listar`, `/usuarios/inserir`, `/financeiro/listar`, `/relatorios/listar` e outras.

As principais responsabilidades do back-end sÃ£o:

- autenticar usuÃ¡rios e controlar sessÃµes;
- proteger rotas administrativas com `login_required`;
- receber dados enviados por formulÃ¡rios;
- validar campos como e-mail, telefone, CPF, datas e valores monetÃ¡rios;
- executar regras de cadastro, ediÃ§Ã£o, inativaÃ§Ã£o e exclusÃ£o lÃ³gica;
- consultar e gravar dados no MySQL;
- gerar relatÃ³rios e respostas de exportaÃ§Ã£o;
- enviar mensagens de retorno ao usuÃ¡rio com `flash`.

O projeto tambÃ©m utiliza recursos do Werkzeug, biblioteca integrada ao ecossistema Flask, para gerar e conferir hashes de senha com `generate_password_hash` e `check_password_hash`, alÃ©m de tratar nomes de arquivos enviados pelo usuÃ¡rio com `secure_filename`.

### 2.5 ROTAS HTTP E API DA APLICAÃ‡ÃƒO

O sistema possui comunicaÃ§Ã£o baseada em rotas HTTP. Tecnicamente, cada rota do Flask funciona como um endpoint da aplicaÃ§Ã£o, pois recebe uma requisiÃ§Ã£o do navegador, executa uma aÃ§Ã£o e retorna uma resposta. Entretanto, o projeto nÃ£o possui uma API REST externa separada em JSON. A comunicaÃ§Ã£o ocorre principalmente por pÃ¡ginas renderizadas no servidor.

Na prÃ¡tica, o funcionamento Ã© o seguinte:

- rotas com mÃ©todo `GET` exibem pÃ¡ginas, formulÃ¡rios, listas, relatÃ³rios e telas do app do usuÃ¡rio;
- rotas com mÃ©todo `POST` recebem dados de formulÃ¡rios e executam alteraÃ§Ãµes;
- apÃ³s cadastros, ediÃ§Ãµes ou exclusÃµes, o sistema redireciona o usuÃ¡rio para a tela correspondente;
- mensagens de sucesso ou erro sÃ£o exibidas com `flash`;
- os relatÃ³rios podem retornar respostas de download, como arquivos em formato Excel ou PDF simples.
- a frente `/app` usa rotas pÃºblicas renderizadas pelo Flask, mas sem expor uma API JSON externa;
- as rotas `/app/oracao/<id>/reagir` e `/app/oracao/<id>/comentar` recebem interaÃ§Ãµes pÃºblicas em pedidos de oraÃ§Ã£o respondidos.

Exemplo do fluxo de cadastro:

```text
UsuÃ¡rio preenche formulÃ¡rio
        |
        v
Navegador envia POST para uma rota Flask
        |
        v
Flask valida os dados recebidos
        |
        v
db.py executa INSERT ou UPDATE no MySQL
        |
        v
Sistema redireciona para a tela adequada e mostra mensagem de retorno
```

Dessa forma, a aplicaÃ§Ã£o possui endpoints internos, mas nÃ£o oferece uma API pÃºblica para consumo por aplicativo mobile nativo, sistema externo ou front-end independente. O app do usuÃ¡rio implementado neste projeto Ã© uma frente web servida pelo prÃ³prio Flask, usando as mesmas tabelas e templates Jinja2. Caso o projeto evolua futuramente, seria possÃ­vel criar uma API REST com respostas JSON para integrar notificaÃ§Ãµes, aplicativos mÃ³veis, serviÃ§os de e-mail, WhatsApp ou gateways de pagamento.

No cadastro pÃºblico, a pessoa nÃ£o recebe acesso administrativo. O formulÃ¡rio grava o registro na tabela `membros` com status `Visitante` e cria um usuÃ¡rio com perfil `VISITANTE`. Ao fazer login, esse perfil Ã© direcionado para o app da igreja, enquanto perfis administrativos sÃ£o direcionados para o painel. Caso um visitante tente acessar uma rota administrativa, o sistema redireciona para `/app`, preservando a separaÃ§Ã£o entre as duas frentes.

### 2.6 PERSISTÃŠNCIA DE DADOS COM MYSQL

O MySQL Ã© um sistema gerenciador de banco de dados relacional utilizado para armazenar informaÃ§Ãµes de forma persistente. Diferentemente de listas em memÃ³ria, os dados gravados no banco permanecem disponÃ­veis mesmo apÃ³s reiniciar a aplicaÃ§Ã£o.

Neste projeto, a conexÃ£o com o MySQL foi centralizada em `db.py`, usando `mysql-connector-python`, pool de conexÃµes e queries parametrizadas com `%s`. O pool de conexÃµes evita que a aplicaÃ§Ã£o precise abrir uma nova conexÃ£o do zero a cada operaÃ§Ã£o, pois mantÃ©m um conjunto de conexÃµes reutilizÃ¡veis com o banco.

As tabelas foram criadas por scripts SQL em `database/migrations`, separando seguranÃ§a, usuÃ¡rios, perfis, permissÃµes e os mÃ³dulos principais de membresia. O banco utiliza chaves primÃ¡rias, chaves estrangeiras, Ã­ndices, campos de data de criaÃ§Ã£o e atualizaÃ§Ã£o, alÃ©m de campos de exclusÃ£o lÃ³gica, como `excluido_em`.

Entre as principais entidades modeladas estÃ£o:

- usuÃ¡rios, perfis e permissÃµes;
- membros, visitantes, famÃ­lias e histÃ³rico espiritual;
- ministÃ©rios, cÃ©lulas, eventos e presenÃ§as;
- fornecedores, lanÃ§amentos financeiros, contas e categorias;
- doaÃ§Ãµes, comunicaÃ§Ã£o, mural, intercessÃ£o e configuraÃ§Ãµes.

A persistÃªncia em banco relacional foi adequada ao projeto porque as informaÃ§Ãµes possuem relaÃ§Ãµes claras, como membro vinculado a famÃ­lia, membro vinculado a ministÃ©rio, doaÃ§Ã£o vinculada a conta financeira e usuÃ¡rio vinculado a perfil.

### 2.7 SEGURANÃ‡A, VALIDAÃ‡ÃƒO E ORGANIZAÃ‡ÃƒO DOS DADOS

A seguranÃ§a do sistema foi tratada por meio de medidas bÃ¡sicas, coerentes com o escopo acadÃªmico da aplicaÃ§Ã£o. O login utiliza sessÃµes do Flask para manter o usuÃ¡rio autenticado, e as rotas administrativas sÃ£o protegidas por um decorador chamado `login_required`.

As senhas nÃ£o sÃ£o armazenadas em texto puro. O sistema grava o hash da senha no banco de dados e, no login, compara a senha digitada com esse hash. Esse processo reduz o risco de exposiÃ§Ã£o direta das senhas em caso de acesso indevido ao banco.

Outra medida aplicada foi o uso de consultas parametrizadas. Em vez de concatenar valores digitados pelo usuÃ¡rio diretamente dentro do SQL, as rotas enviam os parÃ¢metros separadamente para o `mysql-connector-python`. Isso ajuda a reduzir riscos de injeÃ§Ã£o de SQL.

O projeto tambÃ©m utiliza exclusÃ£o lÃ³gica em vÃ¡rios mÃ³dulos. Nessa abordagem, o registro nÃ£o Ã© removido fisicamente do banco; ele recebe uma marcaÃ§Ã£o, como `excluido_em`, ou tem seu status alterado para inativo. Essa escolha preserva histÃ³rico, evita perda acidental de dados e facilita auditoria futura.

### 2.8 TESTES E FERRAMENTAS DE DESENVOLVIMENTO

O desenvolvimento utilizou ferramentas gratuitas e de cÃ³digo aberto. As dependÃªncias Python ficam registradas em `requirements.txt`, incluindo Flask, Jinja2, Werkzeug e mysql-connector-python. O projeto tambÃ©m possui testes automatizados com `unittest`, biblioteca padrÃ£o do Python.

Os testes verificam comportamentos importantes, como renderizaÃ§Ã£o de rotas pÃºblicas, bloqueio de rotas privadas sem login, validaÃ§Ãµes de formulÃ¡rio, redirecionamentos e restriÃ§Ã£o de algumas aÃ§Ãµes ao mÃ©todo POST. Esses testes ajudam a identificar regressÃ£o quando novas funcionalidades sÃ£o adicionadas.

TambÃ©m hÃ¡ testes para validar que o cadastro pÃºblico grava a pessoa como visitante e que a home do app exibe dados alimentados pelas rotas administrativas, como eventos, feed e devocional.

O cÃ³digo-fonte do Sistema de Membresia da Igreja Viva foi versionado e disponibilizado no GitHub, no repositÃ³rio `WellingtonLCR/Projeto_membresia_church`. O perfil do desenvolvedor tambÃ©m fica disponÃ­vel em `github.com/WellingtonLCR`, permitindo consultar o projeto, acompanhar sua evoluÃ§Ã£o e acessar os arquivos usados na entrega acadÃªmica.

TambÃ©m foram usados scripts SQL de migraÃ§Ã£o e seed para organizar a criaÃ§Ã£o do banco. Essa prÃ¡tica facilita reproduzir o ambiente em outro computador, pois a estrutura do banco nÃ£o fica dependente apenas de configuraÃ§Ãµes manuais.

AlÃ©m do seed principal de perfis, permissÃµes, usuÃ¡rio administrador e usuÃ¡rio visitante, o projeto possui seeds demonstrativos com membros, visitantes, ministÃ©rios, cÃ©lulas, eventos, mural, devocional, pedidos de oraÃ§Ã£o, doaÃ§Ãµes e movimentaÃ§Ãµes financeiras. TambÃ©m foi criado um seed histÃ³rico com datas distribuÃ­das entre 2024 e 2026, permitindo testar consultas, filtros, dashboards, relatÃ³rios e a integraÃ§Ã£o entre painel administrativo e app do usuÃ¡rio com dados mais realistas.

### 2.9 USABILIDADE E ORGANIZAÃ‡ÃƒO DA INFORMAÃ‡ÃƒO

A usabilidade Ã© importante para que o usuÃ¡rio consiga localizar funÃ§Ãµes, preencher formulÃ¡rios e interpretar informaÃ§Ãµes sem dificuldade. Por isso, o sistema utiliza menu lateral, cards de mÃ©tricas, tabelas, botÃµes de aÃ§Ã£o, formulÃ¡rios com labels, mensagens de retorno e layout responsivo.

A organizaÃ§Ã£o dos templates por entidade tambÃ©m melhora a manutenibilidade do projeto, pois separa as telas de membros, ministÃ©rios, cÃ©lulas, eventos, financeiro, comunicaÃ§Ã£o e demais mÃ³dulos. Essa divisÃ£o facilita encontrar arquivos, aplicar ajustes pontuais e manter um padrÃ£o visual entre as pÃ¡ginas.

No dashboard e nas listagens, a informaÃ§Ã£o foi organizada para favorecer leitura rÃ¡pida. Os cards apresentam nÃºmeros principais, as tabelas concentram registros administrativos e os botÃµes de aÃ§Ã£o indicam os fluxos mais importantes, como cadastrar, editar, inativar, excluir, publicar, arquivar ou exportar.

### 2.10 VIBE CODING NO DESENVOLVIMENTO DO PROJETO

O projeto tambÃ©m foi desenvolvido com apoio de Vibe Coding, prÃ¡tica recente em que o desenvolvedor descreve objetivos em linguagem natural e utiliza inteligÃªncia artificial para gerar, revisar, adaptar ou explicar trechos de cÃ³digo. Nesse modelo, o foco deixa de ser apenas escrever cada linha manualmente e passa a envolver orientaÃ§Ã£o, revisÃ£o, testes e refinamento da soluÃ§Ã£o gerada.

No Sistema de Membresia da Igreja Viva, o Vibe Coding foi utilizado como apoio para acelerar a criaÃ§Ã£o de telas, rotas, validaÃ§Ãµes, organizaÃ§Ã£o de mÃ³dulos, melhorias de interface, escrita de documentaÃ§Ã£o e revisÃ£o de comportamento. As consultas e interaÃ§Ãµes com ferramentas como ChatGPT e Claude Code auxiliaram no levantamento de alternativas, revisÃ£o textual, anÃ¡lise de padrÃµes de cÃ³digo e implementaÃ§Ã£o incremental. A decisÃ£o final sobre estrutura, escopo e adequaÃ§Ã£o ao projeto permaneceu humana, com verificaÃ§Ã£o no cÃ³digo, execuÃ§Ã£o de testes e alinhamento com os requisitos acadÃªmicos.

As principais vantagens observadas foram:

- maior velocidade para criar estruturas repetitivas, como rotas CRUD, formulÃ¡rios e templates;
- apoio na organizaÃ§Ã£o de ideias e transformaÃ§Ã£o de requisitos em tarefas tÃ©cnicas;
- facilidade para comparar alternativas de implementaÃ§Ã£o;
- ajuda na escrita de documentaÃ§Ã£o, comentÃ¡rios e textos explicativos;
- suporte para identificar pontos de melhoria em seguranÃ§a, validaÃ§Ã£o e usabilidade.

Apesar das vantagens, o uso de Vibe Coding tambÃ©m exige cuidados:

- a IA pode sugerir cÃ³digo que nÃ£o combina com a arquitetura existente;
- algumas respostas podem conter erros, dependÃªncias desnecessÃ¡rias ou soluÃ§Ãµes incompletas;
- Ã© necessÃ¡rio revisar consultas SQL, validaÃ§Ãµes, permissÃµes e regras de seguranÃ§a;
- o desenvolvedor continua responsÃ¡vel por testar e entender o que foi implementado;
- o uso excessivo sem revisÃ£o pode prejudicar a aprendizagem e a manutenibilidade.

Assim, o Vibe Coding foi tratado como uma ferramenta de apoio ao desenvolvimento, e nÃ£o como substituto da anÃ¡lise tÃ©cnica. A prÃ¡tica contribuiu para acelerar a evoluÃ§Ã£o do projeto, mas precisou ser acompanhada por revisÃ£o humana, testes automatizados e verificaÃ§Ã£o da coerÃªncia com Flask, Jinja2, MySQL e os requisitos da disciplina.

## 3. MODELO DE NEGÃ“CIOS

### 3.1 CANVAS

O modelo Canvas foi usado como forma de organizar a proposta do sistema.

- Proposta de valor: centralizar a gestÃ£o administrativa e pastoral da igreja em uma Ãºnica aplicaÃ§Ã£o web.
- Segmento de usuÃ¡rios: secretaria, administradores, lÃ­deres, pastores, equipe financeira e equipe de comunicaÃ§Ã£o.
- Canais: aplicaÃ§Ã£o web acessada pelo navegador em ambiente local.
- Relacionamento com usuÃ¡rios: interface simples, mensagens de feedback, menu organizado e formulÃ¡rios objetivos.
- Atividades principais: cadastro, consulta, atualizaÃ§Ã£o, exclusÃ£o lÃ³gica, relatÃ³rios e controle de processos internos.
- Recursos principais: computador, servidor Flask, banco MySQL, templates Jinja2, Bootstrap e cÃ³digo-fonte do projeto.
- Parcerias principais: Fatec Jahu, disciplina de ProgramaÃ§Ã£o para Internet e equipe de desenvolvimento.
- Estrutura de custos: desenvolvimento acadÃªmico, infraestrutura local, computador, MySQL e manutenÃ§Ã£o futura.
- Fontes de receita: nÃ£o se aplica inicialmente, pois o projeto tem finalidade acadÃªmica.

### 3.2 O QUE SERÃ ELABORADO

SerÃ¡ elaborada uma aplicaÃ§Ã£o web de gestÃ£o de membresia para igrejas, com Ã¡rea pÃºblica, Ã¡rea administrativa protegida por login, mÃ³dulos de cadastro, controles operacionais e relatÃ³rios.

### 3.3 PARA QUEM SERÃ ELABORADO

O sistema foi pensado para igrejas que precisam organizar informaÃ§Ãµes de membros, visitantes, famÃ­lias, ministÃ©rios, cÃ©lulas, eventos, financeiro, comunicaÃ§Ã£o e acompanhamento pastoral.

Os principais usuÃ¡rios sÃ£o:

- Administrador;
- Pastor;
- Secretaria;
- LÃ­der;
- Financeiro;
- Visitante, com acesso ao app do usuÃ¡rio.

### 3.4 COMO SERÃ ELABORADO

O sistema foi elaborado com Python e Flask no back-end, Jinja2 para renderizaÃ§Ã£o de templates, Bootstrap e CSS prÃ³prio na interface, MySQL para persistÃªncia de dados e unittest para testes automatizados.

A estrutura segue o padrÃ£o:

```text
.
|-- app.py
|-- db.py
|-- db_setup.py
|-- requirements.txt
|-- database
|   |-- migrations
|   |-- seeds
|-- static
|   |-- css
|   |-- imgs
|   |-- js
|-- templates
|-- tests
```

### 3.5 QUANTO CUSTARÃ

Por ser um projeto acadÃªmico, nÃ£o hÃ¡ custo comercial inicial. O desenvolvimento foi realizado com ferramentas gratuitas e de cÃ³digo aberto. Em um ambiente real, poderiam existir custos com hospedagem, domÃ­nio, manutenÃ§Ã£o, backups e suporte tÃ©cnico.

## 4. DOCUMENTAÃ‡ÃƒO

### 4.1 DECLARAÃ‡ÃƒO DE ABRANGÃŠNCIA DO PROJETO

O projeto abrange o desenvolvimento de um sistema web para administraÃ§Ã£o de membresia de igreja, contemplando Ã¡rea pÃºblica institucional, app web do usuÃ¡rio, login, painel administrativo e mÃ³dulos de gestÃ£o.

EstÃ£o dentro do escopo:

- app web do usuÃ¡rio com agenda, cultos, feed, devocional, pedidos de oraÃ§Ã£o e informaÃ§Ãµes de doaÃ§Ã£o;
- cadastro e controle de usuÃ¡rios;
- cadastro de membros e visitantes;
- famÃ­lias e vÃ­nculo familiar;
- ministÃ©rios e cÃ©lulas;
- presenÃ§a;
- eventos com banner;
- financeiro, fornecedores e doaÃ§Ãµes;
- comunicaÃ§Ã£o, mural e intercessÃ£o;
- relatÃ³rios;
- configuraÃ§Ãµes administrativas;
- persistÃªncia em MySQL.

NÃ£o fazem parte do escopo atual:

- integraÃ§Ã£o real com WhatsApp, e-mail externo ou gateway de pagamento;
- hospedagem em servidor de produÃ§Ã£o;
- aplicativo mobile nativo;
- controle avanÃ§ado de permissÃµes por tela;
- envio automÃ¡tico de notificaÃ§Ãµes.

### 4.2 Requisitos funcionais

R1. O sistema deve permitir login e logout de usuÃ¡rios administrativos.
R2. O sistema deve permitir cadastro pÃºblico de visitante.
R3. O sistema deve permitir recuperar senha de acesso.
R4. O sistema deve permitir cadastrar usuÃ¡rios com senha provisÃ³ria.
R5. O sistema deve permitir listar, editar, bloquear, inativar e excluir logicamente usuÃ¡rios.
R6. O sistema deve permitir cadastrar, listar, editar, inativar e excluir logicamente membros.
R7. O sistema deve permitir cadastrar e listar visitantes.
R8. O sistema deve permitir registrar histÃ³rico espiritual de membros.
R9. O sistema deve permitir cadastrar famÃ­lias e vincular membros a elas.
R10. O sistema deve permitir cadastrar, listar, editar e excluir logicamente ministÃ©rios.
R11. O sistema deve permitir cadastrar e listar cÃ©lulas.
R12. O sistema deve permitir registrar presenÃ§a por culto, evento ou cÃ©lula.
R13. O sistema deve permitir cadastrar e listar eventos com banner.
R14. O sistema deve permitir cadastrar lanÃ§amentos financeiros de entrada e saÃ­da.
R15. O sistema deve permitir cadastrar fornecedores e vinculÃ¡-los a gastos.
R16. O sistema deve permitir cadastrar doaÃ§Ãµes e baixar doaÃ§Ãµes pendentes para o financeiro.
R17. O sistema deve permitir cadastrar mensagens de comunicaÃ§Ã£o.
R18. O sistema deve permitir cadastrar, publicar e arquivar avisos no mural.
R19. O sistema deve permitir cadastrar pedidos de oraÃ§Ã£o, registrar oraÃ§Ã£o, marcar como respondido e arquivar.
R20. O sistema deve permitir consultar relatÃ³rios e exportar em Excel ou PDF.
R21. O sistema deve permitir editar configuraÃ§Ãµes administrativas da igreja.
R22. O sistema deve disponibilizar painÃ©is por Ã¡rea para Pessoas, Financeiro, MinistÃ©rios, CÃ©lulas, ComunicaÃ§Ã£o e IntercessÃ£o.
R23. O sistema deve separar consultas financeiras em receitas, despesas, movimentaÃ§Ãµes e cadastros auxiliares.
R24. O sistema deve permitir consultar aniversariantes por mÃªs.
R25. O sistema deve permitir consultar testemunhos a partir dos pedidos de oraÃ§Ã£o respondidos.
R26. O sistema deve permitir consultar categorias financeiras, centro de custos, contas bancÃ¡rias, formas de recebimento e formas de pagamento.
R27. O sistema deve organizar as configuraÃ§Ãµes em pÃ¡ginas de igreja, histÃ³ria, informaÃ§Ãµes, programaÃ§Ã£o, permissÃµes, app e mÃ³dulos.
R28. O sistema deve disponibilizar um app web pÃºblico para o usuÃ¡rio final.
R29. O app do usuÃ¡rio deve exibir eventos, cultos, feed, devocional e informaÃ§Ãµes de doaÃ§Ã£o alimentadas pelo painel administrativo.
R30. O app do usuÃ¡rio deve permitir envio pÃºblico de pedido de oraÃ§Ã£o para acompanhamento no mÃ³dulo de intercessÃ£o.
R31. O painel administrativo deve permitir configurar programaÃ§Ã£o fixa e dados de contribuiÃ§Ã£o exibidos no app do usuÃ¡rio.
R32. O painel administrativo deve permitir prÃ©-visualizar a frente pÃºblica do app.
R33. O cadastro feito pelo app do usuÃ¡rio deve registrar a pessoa como visitante no mÃ³dulo de Pessoas.
R34. O sistema deve direcionar usuÃ¡rios administrativos para o painel e visitantes para o app apÃ³s o login.
R35. O app do usuÃ¡rio deve permitir reaÃ§Ãµes e comentÃ¡rios em pedidos de oraÃ§Ã£o respondidos e pÃºblicos.

### 4.3 Requisitos nÃ£o funcionais

RNF1. O sistema deve utilizar banco de dados MySQL real.
RNF2. O sistema deve utilizar SQL parametrizado para reduzir risco de SQL Injection.
RNF3. O sistema deve possuir interface responsiva com Bootstrap.
RNF4. O sistema deve organizar templates com heranÃ§a Jinja2.
RNF5. O sistema deve usar rotas protegidas para Ã¡rea administrativa.
RNF6. O sistema deve exibir mensagens de retorno para aÃ§Ãµes do usuÃ¡rio.
RNF7. O sistema deve manter arquivos estÃ¡ticos em `static` e templates em `templates`.
RNF8. O sistema deve possuir `.gitignore` para evitar versionamento de cache, ambiente virtual e uploads dinÃ¢micos.
RNF9. O sistema deve ter testes automatizados bÃ¡sicos.
RNF10. O sistema deve ser simples de executar em ambiente local.
RNF11. O sistema deve manter identidade visual Ãºnica e consistente em todas as pÃ¡ginas administrativas.
RNF12. O sistema deve permitir alternÃ¢ncia entre tema claro e escuro sem redirecionar o usuÃ¡rio para outra pÃ¡gina.
RNF13. O app do usuÃ¡rio deve reutilizar a mesma infraestrutura Flask, Jinja2 e MySQL, evitando dependÃªncia de framework mobile nativo no escopo atual.
RNF14. A navegaÃ§Ã£o administrativa deve ser agrupada por categorias recolhÃ­veis, reduzindo repetiÃ§Ã£o de menus nas pÃ¡ginas internas.
RNF15. RelatÃ³rios devem ser organizados por categoria, evitando mistura de indicadores de Ã¡reas diferentes no mesmo bloco visual.

### 4.4 Casos de uso

Visitante pÃºblico

- acessar pÃ¡gina inicial;
- acessar app web do usuÃ¡rio;
- visualizar agenda de eventos e detalhes de eventos;
- consultar cultos e programaÃ§Ã£o fixa;
- visualizar feed, comunicados e devocionais publicados;
- enviar pedido de oraÃ§Ã£o para a intercessÃ£o;
- reagir e comentar em testemunhos pÃºblicos;
- consultar informaÃ§Ãµes de doaÃ§Ãµes;
- criar acesso de visitante;
- acessar login e ser direcionado para o app;
- acessar recuperaÃ§Ã£o de senha;
- visualizar pÃ¡gina da equipe.

Administrador

- acessar dashboard;
- gerenciar usuÃ¡rios;
- gerenciar membros e visitantes;
- gerenciar famÃ­lias;
- gerenciar ministÃ©rios;
- gerenciar cÃ©lulas;
- gerenciar eventos;
- registrar presenÃ§as;
- gerenciar financeiro;
- gerenciar fornecedores;
- gerenciar doaÃ§Ãµes;
- gerenciar comunicaÃ§Ã£o;
- gerenciar mural;
- acompanhar intercessÃ£o;
- consultar relatÃ³rios;
- alterar configuraÃ§Ãµes;
- configurar dados do app do usuÃ¡rio;
- prÃ©-visualizar a frente pÃºblica.

Financeiro

- cadastrar entrada;
- cadastrar saÃ­da;
- vincular fornecedor;
- registrar doaÃ§Ã£o;
- baixar doaÃ§Ã£o pendente;
- consultar saldo e movimentaÃ§Ãµes.

LÃ­der

- consultar membros;
- acompanhar cÃ©lulas;
- registrar presenÃ§a;
- consultar eventos;
- acompanhar pedidos de oraÃ§Ã£o.

### 4.5 Modelo conceitual

O modelo conceitual do sistema contempla as seguintes entidades principais:

- UsuÃ¡rios;
- Perfis;
- Igreja;
- Membros;
- FamÃ­lias;
- MinistÃ©rios;
- CÃ©lulas;
- PresenÃ§as;
- Eventos;
- InscriÃ§Ãµes de eventos;
- Categorias financeiras;
- Contas financeiras;
- LanÃ§amentos financeiros;
- Fornecedores;
- DoaÃ§Ãµes;
- Mensagens;
- Mural de avisos;
- Pedidos de oraÃ§Ã£o;
- ReaÃ§Ãµes em pedidos de oraÃ§Ã£o;
- ComentÃ¡rios em pedidos de oraÃ§Ã£o;
- ConfiguraÃ§Ãµes do sistema.
- App web do usuÃ¡rio, como camada de apresentaÃ§Ã£o pÃºblica baseada nessas entidades.

Principais relacionamentos e cardinalidades:

- UsuÃ¡rio e perfil: relaÃ§Ã£o N:N por meio de `usuario_perfil`, pois um usuÃ¡rio pode ter perfil e um perfil pode estar associado a vÃ¡rios usuÃ¡rios.
- Perfil e permissÃ£o: relaÃ§Ã£o N:N por meio de `perfil_permissao`, permitindo agrupar permissÃµes por funÃ§Ã£o.
- Membro e cÃ©lula: relaÃ§Ã£o N:1, pois vÃ¡rios membros podem estar ligados a uma mesma cÃ©lula.
- FamÃ­lia e membros: relaÃ§Ã£o N:N por meio de `familia_membros`, permitindo que uma famÃ­lia tenha vÃ¡rios membros e que o vÃ­nculo registre parentesco.
- Membro e ministÃ©rio: relaÃ§Ã£o N:N por meio de `membro_ministerio`, registrando funÃ§Ã£o, entrada e saÃ­da.
- Evento e inscriÃ§Ãµes: relaÃ§Ã£o 1:N, pois um evento pode possuir vÃ¡rias inscriÃ§Ãµes.
- CÃ©lula e reuniÃµes: relaÃ§Ã£o 1:N, pois uma cÃ©lula pode possuir vÃ¡rias reuniÃµes.
- ReuniÃ£o de cÃ©lula e presenÃ§as: relaÃ§Ã£o N:N por meio de `celula_presencas`.
- LanÃ§amento financeiro e categoria/conta: relaÃ§Ã£o N:1, pois vÃ¡rios lanÃ§amentos pertencem a uma categoria e a uma conta.
- LanÃ§amento financeiro e membro/fornecedor: relaÃ§Ã£o N:1 opcional, pois uma entrada pode estar ligada a membro e uma saÃ­da pode estar ligada a fornecedor.
- DoaÃ§Ã£o e lanÃ§amento financeiro: relaÃ§Ã£o 1:1 opcional, pois uma doaÃ§Ã£o recebida pode gerar um lanÃ§amento financeiro.
- Mensagem e usuÃ¡rio administrativo: relaÃ§Ã£o N:1, pois vÃ¡rias mensagens podem ser criadas por um usuÃ¡rio.
- Mural e usuÃ¡rio administrativo: relaÃ§Ã£o N:1, pois vÃ¡rios avisos podem ser publicados por um usuÃ¡rio.
- Pedido de oraÃ§Ã£o e reaÃ§Ãµes/comentÃ¡rios: relaÃ§Ã£o 1:N, pois um pedido pÃºblico pode receber vÃ¡rias reaÃ§Ãµes e comentÃ¡rios.
- App do usuÃ¡rio e dados administrativos: relaÃ§Ã£o de apresentaÃ§Ã£o, pois eventos, mural, devocionais, pedidos de oraÃ§Ã£o e configuraÃ§Ãµes cadastradas no painel sÃ£o exibidos na frente `/app`.

### 4.6 Benchmarking e melhorias identificadas

Durante o desenvolvimento tambÃ©m foi realizado um estudo visual de sistemas de gestÃ£o eclesiÃ¡stica, reunido em um quadro de benchmarking no tldraw. O material analisado continha telas de referÃªncia inspiradas em plataformas como Eklesia, InPeace e inChurch, observando recursos voltados a membresia, Ã¡rea pastoral, gestÃ£o de intercessÃ£o, igreja, pequenos grupos, ministÃ©rios, eventos, ensinos, comunicaÃ§Ã£o e app para membros.

AlÃ©m dos sites oficiais das plataformas, foram consultadas imagens, protÃ³tipos e materiais internos de apoio ao TCC. Essa anÃ¡lise mostrou padrÃµes recorrentes, como menu lateral por grandes Ã¡reas, formulÃ¡rios divididos em seÃ§Ãµes, app do usuÃ¡rio separado do painel administrativo, mural/devocional, doaÃ§Ãµes, cÃ©lulas, intercessÃ£o e recursos de interaÃ§Ã£o social em conteÃºdos pÃºblicos.

Esse estudo ajudou a perceber que sistemas administrativos para igrejas costumam organizar as funÃ§Ãµes por grandes Ã¡reas de trabalho, cada uma com painel prÃ³prio, telas de gerenciamento, cadastros auxiliares e relatÃ³rios. A partir dessa observaÃ§Ã£o, a documentaÃ§Ã£o do projeto passou a considerar nÃ£o apenas as telas jÃ¡ implementadas, mas tambÃ©m melhorias futuras coerentes com a evoluÃ§Ã£o natural do sistema.

Outro ponto observado foi a existÃªncia de duas frentes de uso: uma frente administrativa, usada por secretaria, lideranÃ§a e financeiro para alimentar dados, e uma frente do usuÃ¡rio, mais simples, voltada para quem deseja acompanhar eventos, cultos, avisos, devocionais, pedidos de oraÃ§Ã£o e contribuiÃ§Ãµes. Essa separaÃ§Ã£o foi aplicada no projeto como app web pÃºblico, sem criar aplicativo mobile nativo ou API externa neste momento.

Menu de referÃªncia estudado:

```text
DASHBOARD

FINANCEIRO
- Painel
- Receitas
- Despesas
- DoaÃ§Ãµes
- MovimentaÃ§Ãµes
- Cadastros
- Categorias
- Centro de Custos
- Contas BancÃ¡rias
- Formas de Recebimento
- Formas de Pagamento
- Fornecedores
- RelatÃ³rios

PESSOAS
- Painel
- Membros
- Visitantes
- AniversÃ¡rios
- RelatÃ³rios

MINISTÃ‰RIOS
- Painel
- Gerenciamento
- RelatÃ³rios

CÃ‰LULAS
- Painel
- Gerenciamento
- RelatÃ³rios

COMUNICAÃ‡ÃƒO
- Painel
- Feed
- Comunicados
- Devocional
- RelatÃ³rios

INTERCESSÃƒO
- Painel
- Pedidos de OraÃ§Ã£o
- Testemunhos
- RelatÃ³rios

CONFIGURAÃ‡Ã•ES
- Igreja
- HistÃ³ria
- InformaÃ§Ãµes
- ProgramaÃ§Ã£o
- PermissÃµes de Acesso
- App
- MÃ³dulos
- Financeiro
- Pessoal
- MinistÃ©rios
- CÃ©lulas
- ComunicaÃ§Ã£o
- IntercessÃ£o
```

Com base nessa anÃ¡lise, foram identificadas as seguintes melhorias para o Sistema de Membresia da Igreja Viva:

| Ãrea | Melhoria identificada | SituaÃ§Ã£o no projeto |
| --- | --- | --- |
| NavegaÃ§Ã£o | Agrupar o menu por Ã¡reas, seguindo o padrÃ£o do benchmarking. | Aplicado no menu lateral desktop e mobile. |
| NavegaÃ§Ã£o | Permitir recolher e expandir categorias do menu para reduzir excesso visual. | Aplicado com grupos recolhÃ­veis no menu lateral. |
| Dashboard | Criar painÃ©is por mÃ³dulo, alÃ©m do dashboard geral. | Aplicado com painÃ©is de Pessoas, Financeiro, MinistÃ©rios, CÃ©lulas, ComunicaÃ§Ã£o e IntercessÃ£o. |
| Financeiro | Separar receitas, despesas, doaÃ§Ãµes, movimentaÃ§Ãµes, cadastros, fornecedores e relatÃ³rios. | Aplicado com rotas especÃ­ficas para painel, receitas, despesas, movimentaÃ§Ãµes e cadastros. |
| Financeiro | Exibir categorias, centro de custos, contas bancÃ¡rias, formas de recebimento e formas de pagamento. | Aplicado com pÃ¡ginas auxiliares protegidas, reaproveitando categorias, contas, doaÃ§Ãµes e lanÃ§amentos existentes. |
| Pessoas | Manter membros e visitantes separados e incluir aniversÃ¡rios. | Aplicado com painel de pessoas e rota de aniversÃ¡rios por mÃªs. |
| MinistÃ©rios | Ter painel do mÃ³dulo, gerenciamento e relatÃ³rios. | Aplicado com painel de ministÃ©rios, cards e lista resumida. |
| CÃ©lulas | Ter painel do mÃ³dulo, gerenciamento, presenÃ§as e relatÃ³rios. | Aplicado com painel de cÃ©lulas e atalhos para gerenciamento e presenÃ§as. |
| ComunicaÃ§Ã£o | Separar feed, comunicados, devocional e relatÃ³rios. | Aplicado usando comunicaÃ§Ã£o e mural como base para feed, comunicados e devocional. |
| IntercessÃ£o | Separar pedidos de oraÃ§Ã£o, testemunhos e relatÃ³rios. | Aplicado com painel de intercessÃ£o e rota de testemunhos baseada em pedidos respondidos. |
| IntercessÃ£o | Permitir reaÃ§Ãµes e comentÃ¡rios em pedidos pÃºblicos, inspirado em interaÃ§Ãµes de app. | Aplicado no app do usuÃ¡rio para testemunhos pÃºblicos. |
| ConfiguraÃ§Ãµes | Organizar igreja, histÃ³ria, informaÃ§Ãµes, programaÃ§Ã£o, permissÃµes, app e mÃ³dulos. | Aplicado com rotas e telas especÃ­ficas para cada grupo de configuraÃ§Ã£o. |
| App do usuÃ¡rio | Criar uma frente pÃºblica diferente do painel administrativo. | Aplicado com rotas `/app`, agenda, cultos, feed, devocional, oraÃ§Ã£o e doaÃ§Ãµes. |
| App do usuÃ¡rio | Direcionar visitantes autenticados para o app e impedir acesso ao painel. | Aplicado com perfil `Visitante`, login direcionado e proteÃ§Ã£o de rotas administrativas. |
| IntegraÃ§Ã£o admin/app | Fazer o painel administrativo alimentar o que o usuÃ¡rio visualiza. | Aplicado usando eventos, mural, pedidos de oraÃ§Ã£o e configuraÃ§Ãµes salvas no MySQL. |
| RelatÃ³rios | Separar indicadores por categoria e melhorar identidade do arquivo gerado. | Aplicado com agrupamento por mÃ³dulo na tela, Excel e PDF. |

As melhorias aplicadas respeitam o escopo acadÃªmico e a arquitetura Flask do projeto. Algumas funcionalidades do benchmarking, como centro de custos completo, CRUD de formas de pagamento, aplicativo mobile nativo, notificaÃ§Ãµes em tempo real e permissÃ£o detalhada por tela, continuam registradas como evoluÃ§Ãµes futuras porque exigiriam novas tabelas, regras, telas especÃ­ficas ou integraÃ§Ãµes externas.

### 4.7 Alinhamento com o plano de estudos da disciplina

O projeto foi mantido alinhado ao material da disciplina ProgramaÃ§Ã£o para Internet, da Fatec Jahu, que organiza o aprendizado em uma progressÃ£o de HTML, Flask, Bootstrap, Jinja2, formulÃ¡rios, MySQL, CRUD, modelagem relacional, seguranÃ§a, login e relatÃ³rios.

O alinhamento pode ser resumido da seguinte forma:

| ConteÃºdo da disciplina | AplicaÃ§Ã£o no projeto |
| --- | --- |
| HTML e Bootstrap | CriaÃ§Ã£o das telas pÃºblicas e administrativas com layout responsivo. |
| Flask e rotas | ImplementaÃ§Ã£o de rotas pÃºblicas, rotas privadas e endpoints de aÃ§Ãµes administrativas. |
| Templates Jinja2 | Uso de `base.html`, `base_publica.html`, `templates/app_usuario/base.html` e templates organizados por mÃ³dulo. |
| FormulÃ¡rios e HTTP | Uso de GET para exibiÃ§Ã£o de telas e POST para cadastros, ediÃ§Ãµes e aÃ§Ãµes. |
| MySQL com Python | ConexÃ£o centralizada em `db.py` usando `mysql-connector-python`. |
| CRUD | Cadastro, listagem, ediÃ§Ã£o, inativaÃ§Ã£o e exclusÃ£o lÃ³gica em vÃ¡rios mÃ³dulos. |
| Modelagem relacional | Uso de tabelas relacionadas, chaves estrangeiras e entidades de associaÃ§Ã£o. |
| VisualizaÃ§Ã£o mestre-detalhe | HistÃ³rico de membro, famÃ­lia com membros, ministÃ©rios e relaÃ§Ãµes de presenÃ§a. |
| SeguranÃ§a e registro | Hash de senha, validaÃ§Ãµes de campos e consultas parametrizadas. |
| Login e sessÃ£o | AutenticaÃ§Ã£o com `session` e proteÃ§Ã£o de rotas com `login_required`. |
| RelatÃ³rios gerenciais | PÃ¡gina de relatÃ³rios, indicadores e exportaÃ§Ã£o simples em Excel/PDF. |
| ExperiÃªncia pÃºblica | App web do usuÃ¡rio com dados vindos das tabelas administradas no painel. |
| ValidaÃ§Ã£o final | Testes automatizados com `unittest` e revisÃ£o dos fluxos principais. |

Assim, o benchmarking foi usado como apoio para melhorar a organizaÃ§Ã£o funcional e visual do sistema, mas a implementaÃ§Ã£o continuou seguindo a trilha tÃ©cnica proposta pela disciplina, sem abandonar Python, Flask, Jinja2, Bootstrap, MySQL, CRUD e relatÃ³rios.

## 5. MANUAL DO USUÃRIO

### 5.1 PreparaÃ§Ã£o do ambiente

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependÃªncias:

```powershell
python -m pip install -r requirements.txt
```

Configure o banco:

```powershell
python db_setup.py
```

Inicie a aplicaÃ§Ã£o:

```powershell
flask --app app run --debug
```

Acesse:

```text
http://127.0.0.1:5000
```

### 5.2 UsuÃ¡rio inicial

UsuÃ¡rio administrador para demonstrar o app:
```text
E-mail: admin@igreja.org
Senha: admin123
```

UsuÃ¡rio visitante para demonstrar o app:

```text
E-mail: visitante@igreja.org
Senha: visitante123
```

### 5.3 PÃ¡gina inicial

A pÃ¡gina inicial apresenta o sistema e permite que o usuÃ¡rio acesse login, cadastro de visitante, equipe e o app web do usuÃ¡rio.

A pÃ¡gina de equipe apresenta os dados do desenvolvedor Wellington LuÃ­s Costa Ribeiro, incluindo contato, atuaÃ§Ã£o no projeto, perfil GitHub disponÃ­vel em `https://github.com/WellingtonLCR` e repositÃ³rio do projeto disponÃ­vel em `https://github.com/WellingtonLCR/Projeto_membresia_church`.

### 5.4 App do usuÃ¡rio

O app do usuÃ¡rio pode ser acessado pela rota `/app`. Ele foi criado como uma frente pÃºblica diferente do painel administrativo, com visual mais simples e adequado para membros, visitantes e pessoas interessadas na programaÃ§Ã£o da igreja.

A navegaÃ§Ã£o do app possui menu superior em telas maiores e menu inferior em dispositivos mÃ³veis, com acesso a inÃ­cio, cultos, agenda, feed, devocional, oraÃ§Ã£o, doaÃ§Ãµes e cadastro de visitante.

No app, o usuÃ¡rio pode:

- visualizar prÃ³ximos eventos cadastrados pela administraÃ§Ã£o;
- abrir detalhes de eventos e cultos;
- acompanhar feed, comunicados e devocionais publicados no mural;
- enviar pedido de oraÃ§Ã£o para a equipe de intercessÃ£o;
- cadastrar-se como visitante, gerando registro no painel administrativo e acesso prÃ³prio ao app;
- reagir e comentar em testemunhos pÃºblicos;
- consultar informaÃ§Ãµes de doaÃ§Ã£o, como PIX, dados bancÃ¡rios e mensagem configurada pelo admin.

O administrador pode prÃ©-visualizar essa frente pelo dashboard, pelo menu lateral ou pela tela de configuraÃ§Ãµes. As informaÃ§Ãµes de programaÃ§Ã£o fixa, doaÃ§Ãµes, eventos, feed e devocionais sÃ£o alimentadas pelo painel administrativo.

### 5.5 Login

Na pÃ¡gina de login, o usuÃ¡rio informa e-mail e senha. ApÃ³s autenticaÃ§Ã£o, perfis administrativos sÃ£o redirecionados para o dashboard do painel. O perfil Visitante Ã© redirecionado para o app do usuÃ¡rio e nÃ£o possui acesso Ã s rotas administrativas.

### 5.6 Dashboard

O dashboard apresenta indicadores gerais e atalhos para os painÃ©is dos mÃ³dulos do sistema. A navegaÃ§Ã£o foi reorganizada conforme o benchmarking estudado, separando as Ã¡reas em Financeiro, Pessoas, MinistÃ©rios, CÃ©lulas, ComunicaÃ§Ã£o, IntercessÃ£o e ConfiguraÃ§Ãµes.

Cada painel de mÃ³dulo apresenta cards de indicadores, atalhos para as principais aÃ§Ãµes e listas resumidas com dados recentes. Essa melhoria permite que o usuÃ¡rio comece pelo painel da Ã¡rea e depois acesse as telas de gerenciamento.

### 5.7 UsuÃ¡rios

O mÃ³dulo de usuÃ¡rios permite cadastrar novos acessos administrativos, definir perfil, informar senha provisÃ³ria, listar usuÃ¡rios e aplicar exclusÃ£o lÃ³gica.

Esse mÃ³dulo Ã© separado do cadastro pÃºblico. Pessoas que se cadastram pelo app entram como visitantes no mÃ³dulo de Pessoas e recebem perfil Visitante, com acesso apenas Ã  frente do usuÃ¡rio.

### 5.8 Membros e visitantes

O mÃ³dulo permite cadastrar pessoas, classificar como membro ou visitante, editar dados, vincular ministÃ©rios e cÃ©lulas, registrar histÃ³rico espiritual e aplicar inativaÃ§Ã£o ou exclusÃ£o lÃ³gica. O painel de pessoas tambÃ©m exibe cadastros recentes, indicadores e aniversariantes do mÃªs.

### 5.9 FamÃ­lias

O usuÃ¡rio pode cadastrar famÃ­lias, definir responsÃ¡vel e vincular membros cadastrados.

### 5.10 MinistÃ©rios

O usuÃ¡rio pode acessar o painel de ministÃ©rios, cadastrar ministÃ©rios, informar lÃ­der, dia de reuniÃ£o, vagas e acompanhar participantes.

### 5.11 CÃ©lulas

O usuÃ¡rio pode acessar o painel de cÃ©lulas, cadastrar cÃ©lulas com lÃ­der, bairro, endereÃ§o, dia e horÃ¡rio de reuniÃ£o, alÃ©m de acompanhar presenÃ§as vinculadas.

### 5.12 PresenÃ§a

O usuÃ¡rio pode registrar presenÃ§a por data, tipo de encontro e membro vinculado.

### 5.13 Eventos

O usuÃ¡rio administrativo pode cadastrar eventos com nome, descriÃ§Ã£o, data, local, status e banner. Eventos nÃ£o cancelados tambÃ©m ficam disponÃ­veis na agenda do app do usuÃ¡rio.

### 5.14 Financeiro

O usuÃ¡rio pode acessar o painel financeiro, consultar receitas, despesas, doaÃ§Ãµes, movimentaÃ§Ãµes e cadastros auxiliares. TambÃ©m pode consultar categorias, centro de custos, contas bancÃ¡rias, formas de recebimento e formas de pagamento. Para cadastrar uma entrada ou saÃ­da, informa categoria, conta, membro ou fornecedor, valor e data.

### 5.15 Fornecedores

O usuÃ¡rio pode cadastrar fornecedores para vincular aos gastos registrados no mÃ³dulo financeiro.

### 5.16 DoaÃ§Ãµes

O usuÃ¡rio administrativo pode registrar doaÃ§Ãµes, definir status, forma de recebimento, recorrÃªncia simples e baixar doaÃ§Ãµes pendentes para o financeiro. No app do usuÃ¡rio, a tela de doaÃ§Ãµes exibe apenas informaÃ§Ãµes de contribuiÃ§Ã£o configuradas pela administraÃ§Ã£o.

### 5.17 ComunicaÃ§Ã£o

O usuÃ¡rio administrativo pode acessar o painel de comunicaÃ§Ã£o, acompanhar feed/mural, cadastrar comunicados, selecionar canal, destino, assunto, corpo e status. O item devocional reaproveita o mural para publicaÃ§Ãµes internas e tambÃ©m aparece no app do usuÃ¡rio quando publicado.

### 5.18 Mural

O usuÃ¡rio pode cadastrar avisos, enviar imagem, publicar ou arquivar comunicados. Avisos publicados aparecem no feed do app do usuÃ¡rio.

### 5.19 IntercessÃ£o

O usuÃ¡rio administrativo pode acessar o painel de intercessÃ£o, registrar pedidos de oraÃ§Ã£o, marcar que orou, indicar que o pedido foi respondido, arquivar e consultar testemunhos a partir dos pedidos respondidos. Pedidos enviados pelo app do usuÃ¡rio entram neste mesmo mÃ³dulo. Testemunhos pÃºblicos podem receber reaÃ§Ãµes e comentÃ¡rios pelo app, e o painel mostra os totais de interaÃ§Ãµes.

### 5.20 RelatÃ³rios

O usuÃ¡rio pode visualizar indicadores operacionais separados por categoria, como Pessoas, EclesiÃ¡stico, Financeiro, ComunicaÃ§Ã£o e IntercessÃ£o. TambÃ©m pode exportar os dados em Excel ou PDF com identidade visual bÃ¡sica e imprimir pelo navegador.

### 5.21 ConfiguraÃ§Ãµes

O usuÃ¡rio pode alterar dados da igreja, parÃ¢metros administrativos, informaÃ§Ãµes do app do usuÃ¡rio e registrar backup lÃ³gico. O menu de configuraÃ§Ãµes tambÃ©m possui pÃ¡ginas especÃ­ficas para igreja, histÃ³ria, informaÃ§Ãµes, programaÃ§Ã£o, permissÃµes de acesso, app e mÃ³dulos ativos.

### 5.22 Testes

Para executar os testes:

```powershell
python -m unittest discover -s tests -q
```

A revisÃ£o final tambÃ©m adicionou testes de entrega dos arquivos estÃ¡ticos essenciais e uma varredura automÃ¡tica das rotas `GET` sem parÃ¢metros com sessÃ£o administrativa autenticada. Essa verificaÃ§Ã£o ajuda a identificar rapidamente pÃ¡ginas quebradas, erros de template, referÃªncias de rota incorretas e falhas de renderizaÃ§Ã£o antes da apresentaÃ§Ã£o.

## 6. CONSIDERAÃ‡Ã•ES FINAIS

O Sistema de Membresia da Igreja Viva atende ao objetivo de centralizar os principais processos administrativos de uma igreja em uma aplicaÃ§Ã£o web. O projeto evoluiu de uma estrutura inicial com telas bÃ¡sicas para uma aplicaÃ§Ã£o com banco MySQL real, mÃ³dulos organizados, aÃ§Ãµes administrativas, relatÃ³rios, validaÃ§Ãµes e uma frente pÃºblica em formato de app web para o usuÃ¡rio final.

A utilizaÃ§Ã£o de Flask, Jinja2, Bootstrap e MySQL permitiu aplicar os conteÃºdos trabalhados na disciplina de ProgramaÃ§Ã£o para Internet de forma prÃ¡tica. O projeto tambÃ©m respeita a estrutura padrÃ£o ensinada nas aulas, com separaÃ§Ã£o entre rotas, templates, arquivos estÃ¡ticos, scripts de banco e testes.

O estudo de sistemas similares, registrado no benchmarking visual, tambÃ©m contribuiu para orientar a evoluÃ§Ã£o da aplicaÃ§Ã£o. A partir dele, foram identificadas melhorias como painÃ©is por mÃ³dulo, reorganizaÃ§Ã£o do menu por Ã¡reas recolhÃ­veis, relatÃ³rios especÃ­ficos, aniversÃ¡rios, testemunhos, devocional, centro de custos, formas de pagamento, formas de recebimento, configuraÃ§Ãµes mais detalhadas da igreja, separaÃ§Ã£o entre painel administrativo e app do usuÃ¡rio, login direcionado por perfil e interaÃ§Ãµes pÃºblicas em pedidos de oraÃ§Ã£o respondidos.

Como evoluÃ§Ãµes futuras, podem ser adicionadas permissÃµes mais detalhadas por perfil, envio real de mensagens, integraÃ§Ã£o com e-mail, dashboards grÃ¡ficos, controle de backups automatizados, deploy em ambiente de produÃ§Ã£o, notificaÃ§Ãµes para o app do usuÃ¡rio e as melhorias planejadas a partir do benchmarking.

### RevisÃ£o final das melhorias implementadas

Na revisÃ£o final do projeto foram incorporadas melhorias visuais e funcionais inspiradas em sistemas profissionais de gestÃ£o eclesiÃ¡stica, como Eklesia, InPeace e inChurch, mantendo a identidade do Sistema de Membresia da Igreja Viva. O login passou a aceitar identificador por e-mail, celular, CPF ou username, mantendo a autenticaÃ§Ã£o protegida por sessÃ£o. O painel administrativo recebeu navegaÃ§Ã£o lateral agrupada por mÃ³dulos, barra superior com breadcrumbs, busca funcional na pÃ¡gina atual, atalhos visuais, microinteraÃ§Ãµes, estados de foco, rodapÃ© padronizado e alternÃ¢ncia real entre tema claro, escuro, alto contraste e preferÃªncia do sistema sem redirecionamento.

TambÃ©m foram revisadas as telas de dashboard, financeiro, doaÃ§Ãµes e cultos. O dashboard passou a apresentar cards de mÃ©tricas, grÃ¡fico visual de pessoas por tipo com legenda por cor, indicadores de engajamento, resumo financeiro e devocionais. O menu mobile foi ajustado para funcionar como offcanvas organizado, com itens principais, estado ativo, Ã­cones e saÃ­da no rodapÃ©. O mÃ³dulo financeiro foi organizado em visÃ£o de competÃªncias, receitas, despesas, movimentaÃ§Ãµes e cadastros auxiliares, com filtros por perÃ­odo, tipo, conta, categoria, status e usuÃ¡rio. O mÃ³dulo de doaÃ§Ãµes recebeu resumo, lista de doaÃ§Ãµes, parcelas, recorrÃªncias, relatÃ³rios e configuraÃ§Ãµes, alÃ©m de fluxos para doador cadastrado, sem cadastro ou anÃ´nimo. O mÃ³dulo de cultos passou a contar com listagem, filtros, cadastro de culto recorrente ou Ãºnico e tela de reuniÃµes.

Durante essa etapa tambÃ©m foi corrigida a referÃªncia de rota `painel_doacoes` no menu lateral. A validaÃ§Ã£o final confirmou que todos os endpoints usados pelo menu existem no `url_map` do Flask, evitando o erro `BuildError` na renderizaÃ§Ã£o do template base.

Para reduzir riscos durante a apresentaÃ§Ã£o, a interface recebeu uma camada local de seguranÃ§a visual e funcional. O arquivo `static/css/styles.css` passou a conter estilos de fallback para botÃµes, modais, offcanvas, filtros, badges, tabelas, cards, tema escuro, alto contraste, estados de foco e estados do menu lateral. O arquivo `static/js/script.js` passou a tratar abertura e fechamento de modais/offcanvas mesmo quando o JavaScript do Bootstrap nÃ£o estiver disponÃ­vel, limpar backdrops travados apÃ³s filtros e impedir que a tela fique bloqueada apÃ³s fechar uma janela. TambÃ©m foram mantidos fallback textual para Ã­cones, recolhimento do menu lateral, foco rÃ¡pido na busca com `Ctrl+K`, troca de tema persistida em `localStorage` e mÃ¡scara simples para campos monetÃ¡rios.

Os dados demonstrativos permanecem centralizados nos scripts de migraÃ§Ã£o e seed executados por `python db_setup.py`, incluindo perfis, permissÃµes, usuÃ¡rios iniciais, membros, visitantes, ministÃ©rios, cÃ©lulas, eventos, mural, devocional, pedidos de oraÃ§Ã£o, doaÃ§Ãµes, lanÃ§amentos financeiros e dados histÃ³ricos de 2024 a 2026. Assim, o projeto pode ser apresentado com ambiente populado e com os principais fluxos administrativos navegÃ¡veis.

## REFERÃŠNCIAS

GTI-Fatec-Jahu. Programacao_Internet-GTI. Material de aulas da disciplina de ProgramaÃ§Ã£o para Internet. DisponÃ­vel em: https://github.com/GTI-Fatec-Jahu/Programacao_Internet-GTI.

PALLETS PROJECTS. Flask Documentation. DisponÃ­vel em: https://flask.palletsprojects.com/.

PALLETS PROJECTS. Jinja Documentation. DisponÃ­vel em: https://jinja.palletsprojects.com/.

ORACLE. MySQL Documentation. DisponÃ­vel em: https://dev.mysql.com/doc/.

ORACLE. MySQL Connector/Python Developer Guide. DisponÃ­vel em: https://dev.mysql.com/doc/connector-python/en/.

BOOTSTRAP TEAM. Bootstrap Documentation. DisponÃ­vel em: https://getbootstrap.com/.

PYTHON SOFTWARE FOUNDATION. Python Documentation. DisponÃ­vel em: https://docs.python.org/.

PYTHON SOFTWARE FOUNDATION. unittest - Unit testing framework. DisponÃ­vel em: https://docs.python.org/3/library/unittest.html.

MOZILLA DEVELOPER NETWORK. HTTP request methods. DisponÃ­vel em: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods.

GOOGLE CLOUD. What is vibe coding? DisponÃ­vel em: https://cloud.google.com/discover/what-is-vibe-coding.

WELLINGTONLCR. Projeto_membresia_church. DisponÃ­vel em: https://github.com/WellingtonLCR/Projeto_membresia_church. Acesso em: 6 jun. 2026.

WELLINGTONLCR. Perfil GitHub. DisponÃ­vel em: https://github.com/WellingtonLCR. Acesso em: 6 jun. 2026.

EKLESIA. SoluÃ§Ãµes para Igrejas. DisponÃ­vel em: https://eklesia.com.br/.

INPEACE. Sistema de GestÃ£o e App para Igrejas. DisponÃ­vel em: https://inpeaceapp.com/.

INCHURCH. LÃ­der em Tecnologia para Igrejas. DisponÃ­vel em: https://www.inchurch.com.br/.

OPENAI. ChatGPT. DisponÃ­vel em: https://chatgpt.com/.

ANTHROPIC. Claude Code Docs. DisponÃ­vel em: https://code.claude.com/docs/en/overview.

TLDRAW. Quadro visual de benchmarking do projeto. DisponÃ­vel em: https://www.tldraw.com/f/8Wn2xu8r8dMCgDB8Y2Bb6?d=v25280.-12746.6944.4095.page.
