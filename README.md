# Sistema de Membresia Church

CENTRO PAULA SOUZA
FACULDADE DE TECNOLOGIA DE JAHU
CURSO DE TECNOLOGIA EM SISTEMAS PARA INTERNET

Wellington Luis Costa Ribeiro

Sistema de Membresia Church

Jaú, SP
2026

## AGRADECIMENTOS

Agradecemos a Faculdade de Tecnologia de Jahu pela estrutura acadêmica e pelo ambiente de aprendizado oferecido durante o desenvolvimento deste projeto.

Agradeço ao Prof. Ronan Adriel Zenatti, orientador deste projeto, pelo material de aula, pelas orientações sobre Flask, Jinja2, MySQL, CRUD, templates, rotas e organização de projeto, que serviram como base para a construção deste sistema.

Agradeço também aos colegas de curso pelas trocas de conhecimento, revisões e sugestões feitas durante a evolução da aplicação.

## RESUMO

O presente projeto tem como objetivo o desenvolvimento de um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e banco de dados MySQL. A aplicação foi criada para centralizar cadastros e processos administrativos que normalmente ficam espalhados em planilhas, controles manuais ou registros informais, dificultando a organização e a consulta das informações.

O sistema permite o gerenciamento de membros, visitantes, famílias, ministérios, células, presenças, eventos, financeiro, fornecedores, doações, comunicação, mural, pedidos de oração, relatórios, usuários e configurações. A persistência dos dados é realizada em banco MySQL real, conforme o conteúdo trabalhado nas aulas, sem uso de listas em memória para os dados principais do projeto.

Durante o desenvolvimento foram aplicados conceitos de rotas públicas e privadas, formulários com métodos GET e POST, herança de templates, mensagens de retorno com flash, SQL parametrizado, exclusão lógica, validações de formulário e organização por templates de entidade. O resultado é uma aplicação funcional, estruturada e alinhada aos requisitos acadêmicos da disciplina.

Palavras-chave: Flask, MySQL, membresia, igreja, CRUD, sistema web.

## ABSTRACT

This project aims to develop a web-based church membership management system using Python, Flask, Jinja2, Bootstrap, and MySQL. The application centralizes administrative records and processes that are commonly handled through spreadsheets, manual controls, or informal records, making information management and consultation more difficult.

The system supports the management of members, visitors, families, ministries, small groups, attendance, events, finances, suppliers, donations, communication, announcements, prayer requests, reports, users, and system settings. Data persistence is handled through a real MySQL database, following the course material, without using in-memory lists for the main project data.

The development process applied concepts such as public and protected routes, GET and POST forms, template inheritance, flash messages, parameterized SQL queries, logical deletion, form validation, and entity-based template organization. The result is a functional and organized web application aligned with the academic requirements of the course.

Keywords: Flask, MySQL, membership, church, CRUD, web system.

## LISTA DE FIGURAS

Figura 1. Modelo Canvas do Sistema de Membresia Church.
Figura 2. Modelo de casos de uso do sistema.
Figura 3. Modelo conceitual do banco de dados.
Figura 4. Página inicial do sistema.
Figura 5. Página de login.
Figura 6. Dashboard administrativo.
Figura 7. Página de membros.
Figura 8. Página de ministérios.
Figura 9. Página de células.
Figura 10. Página de eventos.
Figura 11. Página financeira.
Figura 12. Página de comunicação.
Figura 13. Página de relatórios.
Figura 14. Página de configurações.
Figura 15. Página da equipe.

## SUMÁRIO

1. INTRODUÇÃO
1.1 PROBLEMATIZAÇÃO
1.2 Objetivo geral
1.3 Objetivos específicos
1.4 METODOLOGIA DA PESQUISA
1.5 ESTRUTURA DO TRABALHO
2. REVISÃO BIBLIOGRÁFICA
2.1 SISTEMAS WEB PARA GESTÃO ADMINISTRATIVA
2.2 ARQUITETURA E INFRAESTRUTURA DA APLICAÇÃO
2.3 FRONT-END: HTML, CSS, BOOTSTRAP, JINJA2 E JAVASCRIPT
2.4 BACK-END: PYTHON E FLASK
2.5 ROTAS HTTP E API DA APLICAÇÃO
2.6 PERSISTÊNCIA DE DADOS COM MYSQL
2.7 SEGURANÇA, VALIDAÇÃO E ORGANIZAÇÃO DOS DADOS
2.8 TESTES E FERRAMENTAS DE DESENVOLVIMENTO
2.9 USABILIDADE E ORGANIZAÇÃO DA INFORMAÇÃO
2.10 VIBE CODING NO DESENVOLVIMENTO DO PROJETO
3. MODELO DE NEGÓCIOS
3.1 CANVAS
3.2 O QUE SERÁ ELABORADO
3.3 PARA QUEM SERÁ ELABORADO
3.4 COMO SERÁ ELABORADO
3.5 QUANTO CUSTARA
4. DOCUMENTAÇÃO
4.1 DECLARAÇÃO DE ABRANGÊNCIA DO PROJETO
4.2 Requisitos funcionais
4.3 Requisitos não funcionais
4.4 Casos de uso
4.5 Modelo conceitual
4.6 Benchmarking e melhorias identificadas
4.7 Alinhamento com o plano de estudos da disciplina
5. MANUAL DO USUÁRIO
6. CONSIDERAÇÕES FINAIS
REFERÊNCIAS

## 1. INTRODUÇÃO

Igrejas e organizações religiosas lidam diariamente com informações de membros, visitantes, ministérios, células, eventos, contribuições financeiras, presenças e comunicações internas. Quando esses dados são controlados de forma manual ou descentralizada, a gestão se torna mais lenta, sujeita a erros e difícil de acompanhar.

O Sistema de Membresia Church foi desenvolvido como uma aplicação web para auxiliar a administração de uma igreja local. A proposta é reunir em uma única plataforma os principais cadastros e controles necessários para a secretaria, liderança, ministérios e equipe administrativa.

O projeto utiliza Flask como framework web, Jinja2 para templates HTML, Bootstrap para interface responsiva e MySQL para armazenamento permanente dos dados. A aplicação segue os padrões trabalhados nas aulas de Programação para Internet, especialmente a organização de rotas, templates, formulários, conexão com banco de dados e operações CRUD.

### 1.1 PROBLEMATIZAÇÃO

O controle de membresia pode se tornar complexo quando a igreja cresce e passa a lidar com grande volume de informações. Cadastros duplicados, ausência de histórico, dificuldade para localizar dados, falta de controle de presença, registros financeiros separados e comunicação desorganizada são problemas comuns.

Diante desse contexto, surge a seguinte questão: como desenvolver um sistema web simples, organizado e funcional que permita centralizar os principais processos administrativos de uma igreja, respeitando os conteúdos e requisitos da disciplina?

### 1.2 Objetivo geral

Desenvolver um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e MySQL, com funcionalidades de cadastro, consulta, organização administrativa e relatórios.

### 1.3 Objetivos específicos

- Criar uma aplicação Flask com rotas públicas e rotas protegidas por login.
- Utilizar templates Jinja2 com herança por `base.html` e `base_publica.html`.
- Implementar formulários com validação no back-end.
- Persistir os dados principais em banco MySQL real.
- Criar operações de cadastro, listagem, edição, exclusão lógica e ações administrativas.
- Organizar os templates por entidade, conforme a estrutura ensinada nas aulas.
- Desenvolver uma interface responsiva com Bootstrap e CSS próprio.
- Implementar relatórios com opções de exportação e impressão.
- Registrar testes automatizados para validar rotas e comportamentos principais.

### 1.4 METODOLOGIA DA PESQUISA

O desenvolvimento foi conduzido a partir da análise do material de aula da disciplina de Programação para Internet, com foco nas aulas de Flask, Jinja2, formulários, conexão MySQL, CRUD, autenticação, relatórios e organização de projeto.

Inicialmente, foi definida a estrutura base do sistema, contendo `app.py`, `db.py`, `db_setup.py`, `templates`, `static`, `database` e `tests`. Em seguida, foram modeladas as tabelas principais no MySQL, com scripts de migração e seed para dados iniciais.

As funcionalidades foram implementadas por módulos, seguindo o fluxo:

- levantamento do caso de uso;
- criação ou ajuste da tabela no banco;
- criação da rota Flask;
- criação do template Jinja2;
- validação dos dados recebidos por formulário;
- persistência no MySQL com SQL parametrizado;
- teste de renderização e comportamento.

Também foram analisados projetos de referência em Laravel e Next.js para identificar funcionalidades que poderiam ser trazidas ao sistema sem fugir do escopo acadêmico e sem alterar a arquitetura Flask do projeto.

### 1.5 ESTRUTURA DO TRABALHO

Este README foi organizado seguindo a estrutura do documento de referência:

- O Capítulo 1 apresenta a introdução, problema, objetivos e metodologia.
- O Capítulo 2 apresenta a revisão bibliográfica relacionada ao projeto.
- O Capítulo 3 descreve o modelo de negócios.
- O Capítulo 4 apresenta a documentação técnica e os requisitos.
- O Capítulo 5 apresenta o manual do usuário.
- O Capítulo 6 apresenta as considerações finais.

## 2. REVISÃO BIBLIOGRÁFICA

### 2.1 SISTEMAS WEB PARA GESTÃO ADMINISTRATIVA

Sistemas web permitem que informações sejam acessadas por meio de navegador, sem necessidade de instalacao local em cada computador. Em contextos administrativos, esse modelo facilita o registro, consulta e atualização de dados, além de favorecer a padronizacao dos processos.

No caso de uma igreja, um sistema web pode apoiar a secretaria e a liderança no acompanhamento de membros, visitantes, ministérios, células, eventos e presenças. A centralizacao dessas informações reduz retrabalho e melhora a confiabilidade dos dados.

### 2.2 ARQUITETURA E INFRAESTRUTURA DA APLICAÇÃO

A infraestrutura do Sistema de Membresia Church foi organizada como uma aplicação web monolítica, executada em ambiente local de desenvolvimento. O termo monolítico, neste contexto, indica que a interface, as regras de negócio, as rotas HTTP e o acesso ao banco de dados estão concentrados no mesmo projeto Flask, sem divisão em serviços independentes.

O fluxo principal da aplicação pode ser representado da seguinte forma:

```text
Administracao no navegador              Usuario final no navegador
        |                                      |
        | GET/POST em rotas privadas           | GET/POST em rotas publicas do app
        v                                      v
Painel administrativo Flask              App web do usuario Flask
        |                                      |
        | templates/base.html                  | templates/app_usuario/base.html
        |                                      |
        +--------------- app.py ---------------+
                        |
                        | consultas e gravacoes SQL parametrizadas
                        v
             Camada db.py com mysql-connector-python
                        |
                        v
                  Banco de dados MySQL
```

Nessa estrutura, o navegador acessa páginas do sistema, como login, dashboard, membros, ministérios, células, eventos, financeiro e relatórios. Além da frente administrativa, foi criada uma frente pública em formato de app web para o usuário final, com rotas como `/app`, `/app/eventos`, `/app/cultos`, `/app/feed`, `/app/devocional`, `/app/oracao` e `/app/doacoes`.

O funcionamento segue a lógica observada nos sistemas estudados no benchmarking: o administrador alimenta informações no painel, e o usuário visualiza uma experiência mais simples no app. Eventos cadastrados no admin aparecem na agenda pública, avisos publicados no mural aparecem no feed, publicações de devocional aparecem em uma aba própria, configurações de programação e doações aparecem nas telas de cultos e contribuições, e pedidos enviados pelo app entram na tabela de intercessão para acompanhamento administrativo.

O Flask recebe a requisição, executa as regras necessárias, consulta ou grava dados no MySQL e devolve uma página HTML renderizada pelo Jinja2. Os arquivos estáticos ficam separados na pasta `static`, enquanto as telas ficam organizadas na pasta `templates`.

A estrutura física do projeto reforça essa separação:

- `app.py`: arquivo principal da aplicação, contendo rotas, validações, autenticação e regras dos módulos.
- `db.py`: camada de conexão com o banco MySQL, com pool de conexões e funções auxiliares para consultas.
- `db_setup.py`: script de criação e configuração inicial do banco.
- `database/migrations`: scripts SQL responsáveis pelas tabelas do sistema.
- `database/seeds`: scripts SQL com perfis, permissões, dados iniciais e dados demonstrativos do fluxo admin/app.
- `templates`: páginas HTML renderizadas pelo Flask com Jinja2, incluindo a área administrativa e o app do usuário.
- `static/css`, `static/js` e `static/imgs`: arquivos de estilo, scripts do navegador e imagens.
- `tests`: testes automatizados da aplicação.

Essa organização foi escolhida por ser simples de compreender, adequada ao escopo acadêmico e alinhada ao conteúdo trabalhado na disciplina de Programação para Internet.

### 2.3 FRONT-END: HTML, CSS, BOOTSTRAP, JINJA2 E JAVASCRIPT

O front-end corresponde à parte visual e interativa acessada pelo usuário no navegador. No projeto, ele foi construído com HTML, CSS, Bootstrap, Jinja2 e JavaScript.

O HTML define a estrutura das telas, como formulários, tabelas, menus, botões e cards de métricas. O CSS próprio, localizado em `static/css/styles.css`, complementa o Bootstrap e define identidade visual, cores, espaçamentos, menu lateral, dashboard, tabelas, responsividade e o layout mobile-first do app do usuário. O Bootstrap 5.3.3 foi utilizado por meio de CDN para acelerar a criação de uma interface responsiva, com grid, botões, formulários, alertas, cards, offcanvas e componentes visuais prontos.

O Jinja2 funciona como motor de templates. Ele permite reutilizar estruturas comuns, como `base.html`, `base_publica.html` e `templates/app_usuario/base.html`, e preencher cada página com dados vindos do back-end. Com isso, telas diferentes conseguem compartilhar menu, cabeçalho, rodapé, mensagens de retorno e padrão visual, reduzindo repetição de código.

O JavaScript do projeto, localizado em `static/js/script.js`, foi usado de forma pontual para melhorar a experiência do usuário. Entre os recursos implementados estão a confirmação antes de excluir registros e a indicação de força de senha durante o cadastro. A aplicação não depende de um framework front-end separado, como React, Vue ou Angular, pois a renderização principal acontece no servidor Flask.

### 2.4 BACK-END: PYTHON E FLASK

O back-end é a camada responsável por processar as regras do sistema. Neste projeto, ele foi desenvolvido em Python, utilizando o framework Flask. O Python foi escolhido por sua sintaxe simples, boa legibilidade e forte uso em aplicações web, automação, testes e integração com bancos de dados.

O Flask foi utilizado para criar as rotas da aplicação, receber requisições HTTP, controlar sessões de usuário, validar formulários, renderizar templates e redirecionar o usuário após cada operação. O arquivo `app.py` concentra as rotas principais, como `/login`, `/dashboard`, `/membros/listar`, `/usuarios/inserir`, `/financeiro/listar`, `/relatorios/listar` e outras.

As principais responsabilidades do back-end são:

- autenticar usuários e controlar sessões;
- proteger rotas administrativas com `login_required`;
- receber dados enviados por formulários;
- validar campos como e-mail, telefone, CPF, datas e valores monetários;
- executar regras de cadastro, edição, inativação e exclusão lógica;
- consultar e gravar dados no MySQL;
- gerar relatórios e respostas de exportação;
- enviar mensagens de retorno ao usuário com `flash`.

O projeto também utiliza recursos do Werkzeug, biblioteca integrada ao ecossistema Flask, para gerar e conferir hashes de senha com `generate_password_hash` e `check_password_hash`, além de tratar nomes de arquivos enviados pelo usuário com `secure_filename`.

### 2.5 ROTAS HTTP E API DA APLICAÇÃO

O sistema possui comunicação baseada em rotas HTTP. Tecnicamente, cada rota do Flask funciona como um endpoint da aplicação, pois recebe uma requisição do navegador, executa uma ação e retorna uma resposta. Entretanto, o projeto não possui uma API REST externa separada em JSON. A comunicação ocorre principalmente por páginas renderizadas no servidor.

Na prática, o funcionamento é o seguinte:

- rotas com método `GET` exibem páginas, formulários, listas, relatórios e telas do app do usuário;
- rotas com método `POST` recebem dados de formulários e executam alterações;
- após cadastros, edições ou exclusões, o sistema redireciona o usuário para a tela correspondente;
- mensagens de sucesso ou erro são exibidas com `flash`;
- os relatórios podem retornar respostas de download, como arquivos em formato Excel ou PDF simples.
- a frente `/app` usa rotas públicas renderizadas pelo Flask, mas sem expor uma API JSON externa.

Exemplo do fluxo de cadastro:

```text
Usuário preenche formulário
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

Dessa forma, a aplicação possui endpoints internos, mas não oferece uma API pública para consumo por aplicativo mobile nativo, sistema externo ou front-end independente. O app do usuário implementado neste projeto é uma frente web servida pelo próprio Flask, usando as mesmas tabelas e templates Jinja2. Caso o projeto evolua futuramente, seria possível criar uma API REST com respostas JSON para integrar notificações, aplicativos móveis, serviços de e-mail, WhatsApp ou gateways de pagamento.

No cadastro público, a pessoa não recebe acesso administrativo. O formulário grava o registro na tabela `membros` com status `Visitante`, permitindo que a secretaria acompanhe esse contato pelo painel de Pessoas/Visitantes.

### 2.6 PERSISTÊNCIA DE DADOS COM MYSQL

O MySQL é um sistema gerenciador de banco de dados relacional utilizado para armazenar informações de forma persistente. Diferentemente de listas em memória, os dados gravados no banco permanecem disponíveis mesmo após reiniciar a aplicação.

Neste projeto, a conexão com o MySQL foi centralizada em `db.py`, usando `mysql-connector-python`, pool de conexões e queries parametrizadas com `%s`. O pool de conexões evita que a aplicação precise abrir uma nova conexão do zero a cada operação, pois mantém um conjunto de conexões reutilizáveis com o banco.

As tabelas foram criadas por scripts SQL em `database/migrations`, separando segurança, usuários, perfis, permissões e os módulos principais de membresia. O banco utiliza chaves primárias, chaves estrangeiras, índices, campos de data de criação e atualização, além de campos de exclusão lógica, como `excluido_em`.

Entre as principais entidades modeladas estão:

- usuários, perfis e permissões;
- membros, visitantes, famílias e histórico espiritual;
- ministérios, células, eventos e presenças;
- fornecedores, lançamentos financeiros, contas e categorias;
- doações, comunicação, mural, intercessão e configurações.

A persistência em banco relacional foi adequada ao projeto porque as informações possuem relações claras, como membro vinculado a família, membro vinculado a ministério, doação vinculada a conta financeira e usuário vinculado a perfil.

### 2.7 SEGURANÇA, VALIDAÇÃO E ORGANIZAÇÃO DOS DADOS

A segurança do sistema foi tratada por meio de medidas básicas, coerentes com o escopo acadêmico da aplicação. O login utiliza sessões do Flask para manter o usuário autenticado, e as rotas administrativas são protegidas por um decorador chamado `login_required`.

As senhas não são armazenadas em texto puro. O sistema grava o hash da senha no banco de dados e, no login, compara a senha digitada com esse hash. Esse processo reduz o risco de exposição direta das senhas em caso de acesso indevido ao banco.

Outra medida aplicada foi o uso de consultas parametrizadas. Em vez de concatenar valores digitados pelo usuário diretamente dentro do SQL, as rotas enviam os parâmetros separadamente para o `mysql-connector-python`. Isso ajuda a reduzir riscos de injeção de SQL.

O projeto também utiliza exclusão lógica em vários módulos. Nessa abordagem, o registro não e removido fisicamente do banco; ele recebe uma marcação, como `excluido_em`, ou tem seu status alterado para inativo. Essa escolha preserva histórico, evita perda acidental de dados e facilita auditoria futura.

### 2.8 TESTES E FERRAMENTAS DE DESENVOLVIMENTO

O desenvolvimento utilizou ferramentas gratuitas e de código aberto. As dependências Python ficam registradas em `requirements.txt`, incluindo Flask, Jinja2, Werkzeug e mysql-connector-python. O projeto também possui testes automatizados com `unittest`, biblioteca padrão do Python.

Os testes verificam comportamentos importantes, como renderização de rotas públicas, bloqueio de rotas privadas sem login, validações de formulário, redirecionamentos e restrição de algumas ações ao método POST. Esses testes ajudam a identificar regressão quando novas funcionalidades são adicionadas.

Também há testes para validar que o cadastro público grava a pessoa como visitante e que a home do app exibe dados alimentados pelas rotas administrativas, como eventos, feed e devocional.

Também foram usados scripts SQL de migração e seed para organizar a criação do banco. Essa prática facilita reproduzir o ambiente em outro computador, pois a estrutura do banco não fica dependente apenas de configurações manuais.

Além do seed principal de perfis, permissões e usuário administrador, o projeto possui um seed demonstrativo com membros, visitantes, ministérios, células, eventos, mural, devocional, pedidos de oração, doações e movimentações financeiras. Esses dados permitem apresentar o sistema com números no dashboard e conteúdo visível no app do usuário.

### 2.9 USABILIDADE E ORGANIZAÇÃO DA INFORMAÇÃO

A usabilidade é importante para que o usuário consiga localizar funções, preencher formulários e interpretar informações sem dificuldade. Por isso, o sistema utiliza menu lateral, cards de métricas, tabelas, botões de ação, formulários com labels, mensagens de retorno e layout responsivo.

A organização dos templates por entidade também melhora a manutenibilidade do projeto, pois separa as telas de membros, ministérios, células, eventos, financeiro, comunicação e demais módulos. Essa divisão facilita encontrar arquivos, aplicar ajustes pontuais e manter um padrão visual entre as páginas.

No dashboard e nas listagens, a informação foi organizada para favorecer leitura rápida. Os cards apresentam números principais, as tabelas concentram registros administrativos e os botões de ação indicam os fluxos mais importantes, como cadastrar, editar, inativar, excluir, publicar, arquivar ou exportar.

### 2.10 VIBE CODING NO DESENVOLVIMENTO DO PROJETO

O projeto também foi desenvolvido com apoio de Vibe Coding, prática recente em que o desenvolvedor descreve objetivos em linguagem natural e utiliza inteligência artificial para gerar, revisar, adaptar ou explicar trechos de código. Nesse modelo, o foco deixa de ser apenas escrever cada linha manualmente e passa a envolver orientação, revisão, testes e refinamento da solução gerada.

No Sistema de Membresia Church, o Vibe Coding foi utilizado como apoio para acelerar a criação de telas, rotas, validações, organização de módulos, melhorias de interface, escrita de documentação e revisão de comportamento. A decisão final sobre estrutura, escopo e adequação ao projeto permaneceu humana, com verificação no código, execução de testes e alinhamento com os requisitos acadêmicos.

As principais vantagens observadas foram:

- maior velocidade para criar estruturas repetitivas, como rotas CRUD, formulários e templates;
- apoio na organização de ideias e transformação de requisitos em tarefas técnicas;
- facilidade para comparar alternativas de implementação;
- ajuda na escrita de documentação, comentários e textos explicativos;
- suporte para identificar pontos de melhoria em segurança, validação e usabilidade.

Apesar das vantagens, o uso de Vibe Coding também exige cuidados:

- a IA pode sugerir código que não combina com a arquitetura existente;
- algumas respostas podem conter erros, dependências desnecessárias ou soluções incompletas;
- é necessário revisar consultas SQL, validações, permissões e regras de segurança;
- o desenvolvedor continua responsável por testar e entender o que foi implementado;
- o uso excessivo sem revisão pode prejudicar a aprendizagem e a manutenibilidade.

Assim, o Vibe Coding foi tratado como uma ferramenta de apoio ao desenvolvimento, e não como substituto da análise técnica. A prática contribuiu para acelerar a evolução do projeto, mas precisou ser acompanhada por revisão humana, testes automatizados e verificação da coerência com Flask, Jinja2, MySQL e os requisitos da disciplina.

## 3. MODELO DE NEGÓCIOS

### 3.1 CANVAS

O modelo Canvas foi usado como forma de organizar a proposta do sistema.

- Proposta de valor: centralizar a gestão administrativa e pastoral da igreja em uma única aplicação web.
- Segmento de usuários: secretaria, administradores, líderes, pastores, equipe financeira e equipe de comunicação.
- Canais: aplicação web acessada pelo navegador em ambiente local.
- Relacionamento com usuários: interface simples, mensagens de feedback, menu organizado e formulários objetivos.
- Atividades principais: cadastro, consulta, atualização, exclusão lógica, relatórios e controle de processos internos.
- Recursos principais: computador, servidor Flask, banco MySQL, templates Jinja2, Bootstrap e código-fonte do projeto.
- Parcerias principais: Fatec Jahu, disciplina de Programação para Internet e equipe de desenvolvimento.
- Estrutura de custos: desenvolvimento acadêmico, infraestrutura local, computador, MySQL e manutencao futura.
- Fontes de receita: não se aplica inicialmente, pois o projeto tem finalidade acadêmica.

### 3.2 O QUE SERA ELABORADO

Será elaborada uma aplicação web de gestão de membresia para igrejas, com área pública, área administrativa protegida por login, módulos de cadastro, controles operacionais e relatórios.

### 3.3 PARA QUEM SERA ELABORADO

O sistema foi pensado para igrejas que precisam organizar informações de membros, visitantes, famílias, ministérios, células, eventos, financeiro, comunicação e acompanhamento pastoral.

Os principais usuários são:

- Administrador;
- Pastor;
- Secretaria;
- Lider;
- Financeiro.

### 3.4 COMO SERA ELABORADO

O sistema foi elaborado com Python e Flask no back-end, Jinja2 para renderização de templates, Bootstrap e CSS próprio na interface, MySQL para persistência de dados e unittest para testes automatizados.

A estrutura segue o padrão:

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

### 3.5 QUANTO CUSTARA

Por ser um projeto acadêmico, não ha custo comercial inicial. O desenvolvimento foi realizado com ferramentas gratuitas e de código aberto. Em um ambiente real, poderiam existir custos com hospedagem, dominio, manutencao, backups e suporte tecnico.

## 4. DOCUMENTAÇÃO

### 4.1 DECLARACAO DE ABRANGENCIA DO PROJETO

O projeto abrange o desenvolvimento de um sistema web para administração de membresia de igreja, contemplando área pública institucional, app web do usuário, login, painel administrativo e módulos de gestão.

Estao dentro do escopo:

- app web do usuário com agenda, cultos, feed, devocional, pedidos de oração e informações de doação;
- cadastro e controle de usuários;
- cadastro de membros e visitantes;
- famílias e vínculo familiar;
- ministérios e células;
- presença;
- eventos com banner;
- financeiro, fornecedores e doações;
- comunicação, mural e intercessão;
- relatórios;
- configurações administrativas;
- persistência em MySQL.

Não fazem parte do escopo atual:

- integração real com WhatsApp, e-mail externo ou gateway de pagamento;
- hospedagem em servidor de produção;
- aplicativo mobile nativo;
- controle avançado de permissões por tela;
- envio automático de notificações.

### 4.2 Requisitos funcionais

R1. O sistema deve permitir login e logout de usuários administrativos.
R2. O sistema deve permitir cadastro público de visitante.
R3. O sistema deve permitir recuperar senha de acesso.
R4. O sistema deve permitir cadastrar usuários com senha provisória.
R5. O sistema deve permitir listar, editar, bloquear, inativar e excluir logicamente usuários.
R6. O sistema deve permitir cadastrar, listar, editar, inativar e excluir logicamente membros.
R7. O sistema deve permitir cadastrar e listar visitantes.
R8. O sistema deve permitir registrar histórico espiritual de membros.
R9. O sistema deve permitir cadastrar famílias e vincular membros a elas.
R10. O sistema deve permitir cadastrar, listar, editar e excluir logicamente ministérios.
R11. O sistema deve permitir cadastrar e listar células.
R12. O sistema deve permitir registrar presença por culto, evento ou célula.
R13. O sistema deve permitir cadastrar e listar eventos com banner.
R14. O sistema deve permitir cadastrar lançamentos financeiros de entrada e saída.
R15. O sistema deve permitir cadastrar fornecedores e vinculá-los a gastos.
R16. O sistema deve permitir cadastrar doações e baixar doações pendentes para o financeiro.
R17. O sistema deve permitir cadastrar mensagens de comunicação.
R18. O sistema deve permitir cadastrar, publicar e arquivar avisos no mural.
R19. O sistema deve permitir cadastrar pedidos de oração, registrar oração, marcar como respondido e arquivar.
R20. O sistema deve permitir consultar relatórios e exportar em Excel ou PDF.
R21. O sistema deve permitir editar configurações administrativas da igreja.
R22. O sistema deve disponibilizar painéis por área para Pessoas, Financeiro, Ministérios, Células, Comunicação e Intercessão.
R23. O sistema deve separar consultas financeiras em receitas, despesas, movimentações e cadastros auxiliares.
R24. O sistema deve permitir consultar aniversariantes por mês.
R25. O sistema deve permitir consultar testemunhos a partir dos pedidos de oração respondidos.
R26. O sistema deve permitir consultar categorias financeiras, centro de custos, contas bancárias, formas de recebimento e formas de pagamento.
R27. O sistema deve organizar as configurações em páginas de igreja, história, informações, programação, permissões, app e módulos.
R28. O sistema deve disponibilizar um app web público para o usuário final.
R29. O app do usuário deve exibir eventos, cultos, feed, devocional e informações de doação alimentadas pelo painel administrativo.
R30. O app do usuário deve permitir envio público de pedido de oração para acompanhamento no módulo de intercessão.
R31. O painel administrativo deve permitir configurar programação fixa e dados de contribuição exibidos no app do usuário.
R32. O painel administrativo deve permitir pré-visualizar a frente pública do app.
R33. O cadastro feito pelo app do usuário deve registrar a pessoa como visitante no módulo de Pessoas.

### 4.3 Requisitos não funcionais

RNF1. O sistema deve utilizar banco de dados MySQL real.
RNF2. O sistema deve utilizar SQL parametrizado para reduzir risco de SQL Injection.
RNF3. O sistema deve possuir interface responsiva com Bootstrap.
RNF4. O sistema deve organizar templates com herança Jinja2.
RNF5. O sistema deve usar rotas protegidas para área administrativa.
RNF6. O sistema deve exibir mensagens de retorno para ações do usuário.
RNF7. O sistema deve manter arquivos estáticos em `static` e templates em `templates`.
RNF8. O sistema deve possuir `.gitignore` para evitar versionamento de cache, ambiente virtual e uploads dinamicos.
RNF9. O sistema deve ter testes automatizados básicos.
RNF10. O sistema deve ser simples de executar em ambiente local.
RNF11. O app do usuário deve reutilizar a mesma infraestrutura Flask, Jinja2 e MySQL, evitando dependência de framework mobile nativo no escopo atual.

### 4.4 Casos de uso

Visitante público

- acessar página inicial;
- acessar app web do usuário;
- visualizar agenda de eventos e detalhes de eventos;
- consultar cultos e programação fixa;
- visualizar feed, comunicados e devocionais publicados;
- enviar pedido de oração para a intercessão;
- consultar informações de doações;
- acessar login;
- acessar cadastro;
- acessar recuperação de senha;
- visualizar página da equipe.

Administrador

- acessar dashboard;
- gerenciar usuários;
- gerenciar membros e visitantes;
- gerenciar famílias;
- gerenciar ministérios;
- gerenciar células;
- gerenciar eventos;
- registrar presenças;
- gerenciar financeiro;
- gerenciar fornecedores;
- gerenciar doações;
- gerenciar comunicação;
- gerenciar mural;
- acompanhar intercessão;
- consultar relatórios;
- alterar configurações;
- configurar dados do app do usuário;
- pré-visualizar a frente pública.

Financeiro

- cadastrar entrada;
- cadastrar saída;
- vincular fornecedor;
- registrar doação;
- baixar doação pendente;
- consultar saldo e movimentações.

Lider

- consultar membros;
- acompanhar células;
- registrar presença;
- consultar eventos;
- acompanhar pedidos de oração.

### 4.5 Modelo conceitual

O modelo conceitual do sistema contempla as seguintes entidades principais:

- Usuários;
- Perfis;
- Igreja;
- Membros;
- Famílias;
- Ministérios;
- Células;
- Presenças;
- Eventos;
- Inscricoes de eventos;
- Categorias financeiras;
- Contas financeiras;
- Lancamentos financeiros;
- Fornecedores;
- Doações;
- Mensagens;
- Mural de avisos;
- Pedidos de oração;
- Configurações do sistema.
- App web do usuário, como camada de apresentacao pública baseada nessas entidades.

Principais relacionamentos:

- Um usuário possui perfil.
- Um membro pode estar vinculado a uma célula.
- Um membro pode participar de vários ministérios.
- Uma família pode possuir vários membros.
- Um evento pode possuir inscricoes.
- Um lancamento financeiro pode estar vinculado a membro, conta, categoria e fornecedor.
- Uma doação pode gerar lancamento financeiro.
- Uma mensagem pode ser enviada por usuário administrativo.
- Um aviso de mural pode ser criado por usuário administrativo.
- Um evento, aviso, devocional, configuração de programação ou configuração de doação cadastrado no admin pode ser exibido no app do usuário.
- Um pedido de oração enviado pelo app do usuário pode ser acompanhado no módulo administrativo de intercessão.

### 4.6 Benchmarking e melhorias identificadas

Durante o desenvolvimento também foi realizado um estudo visual de sistemas de gestão eclesiástica, reunido em um quadro de benchmarking no tldraw. O material analisado continha telas de referência inspiradas em plataformas como Ekklesia, InPeace e InChurch, observando recursos voltados a membresia, área pastoral, gestão de intercessão, igreja, pequenos grupos, ministérios, eventos, ensinos, comunicação e app para membros.

Esse estudo ajudou a perceber que sistemas administrativos para igrejas costumam organizar as funções por grandes áreas de trabalho, cada uma com painel próprio, telas de gerenciamento, cadastros auxiliares e relatórios. A partir dessa observação, a documentação do projeto passou a considerar não apenas as telas já implementadas, mas também melhorias futuras coerentes com a evolução natural do sistema.

Outro ponto observado foi a existência de duas frentes de uso: uma frente administrativa, usada por secretaria, liderança e financeiro para alimentar dados, e uma frente do usuário, mais simples, voltada para quem deseja acompanhar eventos, cultos, avisos, devocionais, pedidos de oração e contribuições. Essa separação foi aplicada no projeto como app web público, sem criar aplicativo mobile nativo ou API externa neste momento.

Menu de referência estudado:

```text
DASHBOARD

FINANCEIRO
- Painel
- Receitas
- Despesas
- Doações
- Movimentações
- Cadastros
- Categorias
- Centro de Custos
- Contas Bancárias
- Formas de Recebimento
- Formas de Pagamento
- Fornecedores
- Relatórios

PESSOAS
- Painel
- Membros
- Visitantes
- Aniversários
- Relatórios

MINISTÉRIOS
- Painel
- Gerenciamento
- Relatórios

CÉLULAS
- Painel
- Gerenciamento
- Relatórios

COMUNICAÇÃO
- Painel
- Feed
- Comunicados
- Devocional
- Relatórios

INTERCESSÃO
- Painel
- Pedidos de Oração
- Testemunhos
- Relatórios

CONFIGURAÇÕES
- Igreja
- História
- Informações
- Programação
- Permissões de Acesso
- App
- Módulos
- Financeiro
- Pessoal
- Ministérios
- Células
- Comunicação
- Intercessão
```

Com base nessa análise, foram identificadas as seguintes melhorias para o Sistema de Membresia Church:

| Área | Melhoria identificada | Situação no projeto |
| --- | --- | --- |
| Navegação | Agrupar o menu por áreas, seguindo o padrão do benchmarking. | Aplicado no menu lateral desktop e mobile. |
| Dashboard | Criar painéis por módulo, além do dashboard geral. | Aplicado com painéis de Pessoas, Financeiro, Ministérios, Células, Comunicação e Intercessão. |
| Financeiro | Separar receitas, despesas, doações, movimentações, cadastros, fornecedores e relatórios. | Aplicado com rotas específicas para painel, receitas, despesas, movimentações e cadastros. |
| Financeiro | Exibir categorias, centro de custos, contas bancárias, formas de recebimento e formas de pagamento. | Aplicado com páginas auxiliares protegidas, reaproveitando categorias, contas, doações e lançamentos existentes. |
| Pessoas | Manter membros e visitantes separados e incluir aniversários. | Aplicado com painel de pessoas e rota de aniversários por mês. |
| Ministérios | Ter painel do módulo, gerenciamento e relatórios. | Aplicado com painel de ministérios, cards e lista resumida. |
| Células | Ter painel do módulo, gerenciamento, presenças e relatórios. | Aplicado com painel de células e atalhos para gerenciamento e presenças. |
| Comunicação | Separar feed, comunicados, devocional e relatórios. | Aplicado usando comunicação e mural como base para feed, comunicados e devocional. |
| Intercessão | Separar pedidos de oração, testemunhos e relatórios. | Aplicado com painel de intercessão e rota de testemunhos baseada em pedidos respondidos. |
| Configurações | Organizar igreja, história, informações, programação, permissões, app e módulos. | Aplicado com rotas e telas específicas para cada grupo de configuração. |
| App do usuário | Criar uma frente pública diferente do painel administrativo. | Aplicado com rotas `/app`, agenda, cultos, feed, devocional, oração e doações. |
| Integração admin/app | Fazer o painel administrativo alimentar o que o usuário visualiza. | Aplicado usando eventos, mural, pedidos de oração e configurações salvas no MySQL. |

As melhorias aplicadas respeitam o escopo acadêmico e a arquitetura Flask do projeto. Algumas funcionalidades do benchmarking, como centro de custos completo, CRUD de formas de pagamento, aplicativo mobile nativo, notificações em tempo real e permissão detalhada por tela, continuam registradas como evoluções futuras porque exigiriam novas tabelas, regras, telas específicas ou integrações externas.

### 4.7 Alinhamento com o plano de estudos da disciplina

O projeto foi mantido alinhado ao material da disciplina Programação para Internet, da Fatec Jahu, que organiza o aprendizado em uma progressão de HTML, Flask, Bootstrap, Jinja2, formulários, MySQL, CRUD, modelagem relacional, segurança, login e relatórios.

O alinhamento pode ser resumido da seguinte forma:

| Conteúdo da disciplina | Aplicação no projeto |
| --- | --- |
| HTML e Bootstrap | Criação das telas públicas e administrativas com layout responsivo. |
| Flask e rotas | Implementação de rotas públicas, rotas privadas e endpoints de ações administrativas. |
| Templates Jinja2 | Uso de `base.html`, `base_publica.html`, `templates/app_usuario/base.html` e templates organizados por módulo. |
| Formulários e HTTP | Uso de GET para exibição de telas e POST para cadastros, edições e ações. |
| MySQL com Python | Conexão centralizada em `db.py` usando `mysql-connector-python`. |
| CRUD | Cadastro, listagem, edição, inativação e exclusão lógica em vários módulos. |
| Modelagem relacional | Uso de tabelas relacionadas, chaves estrangeiras e entidades de associação. |
| Visualização mestre-detalhe | Histórico de membro, família com membros, ministérios e relações de presença. |
| Segurança e registro | Hash de senha, validações de campos e consultas parametrizadas. |
| Login e sessão | Autenticação com `session` e proteção de rotas com `login_required`. |
| Relatórios gerenciais | Página de relatórios, indicadores e exportação simples em Excel/PDF. |
| Experiência pública | App web do usuário com dados vindos das tabelas administradas no painel. |
| Validação final | Testes automatizados com `unittest` e revisão dos fluxos principais. |

Assim, o benchmarking foi usado como apoio para melhorar a organização funcional e visual do sistema, mas a implementação continuou seguindo a trilha técnica proposta pela disciplina, sem abandonar Python, Flask, Jinja2, Bootstrap, MySQL, CRUD e relatórios.

## 5. MANUAL DO USUÁRIO

### 5.1 Preparacao do ambiente

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Configure o banco:

```powershell
python db_setup.py
```

Inicie a aplicação:

```powershell
flask --app app run --debug
```

Acesse:

```text
http://127.0.0.1:5000
```

### 5.2 Usuário inicial

```text
E-mail: admin@igreja.org
Senha: admin123
```

### 5.3 Página inicial

A página inicial apresenta o sistema e permite que o usuário acesse login, cadastro de visitante, equipe e o app web do usuário.

### 5.4 App do usuário

O app do usuário pode ser acessado pela rota `/app`. Ele foi criado como uma frente pública diferente do painel administrativo, com visual mais simples e adequado para membros, visitantes e pessoas interessadas na programação da igreja.

A navegação do app possui menu superior em telas maiores e menu inferior em dispositivos móveis, com acesso a início, cultos, agenda, feed, devocional, oração, doações e cadastro de visitante.

No app, o usuário pode:

- visualizar próximos eventos cadastrados pela administração;
- abrir detalhes de eventos e cultos;
- acompanhar feed, comunicados e devocionais publicados no mural;
- enviar pedido de oração para a equipe de intercessão;
- cadastrar-se como visitante, gerando registro no painel administrativo;
- consultar informações de doação, como PIX, dados bancários e mensagem configurada pelo admin.

O administrador pode pré-visualizar essa frente pelo dashboard, pelo menu lateral ou pela tela de configurações. As informações de programação fixa, doações, eventos, feed e devocionais são alimentadas pelo painel administrativo.

### 5.5 Login

Na página de login, o usuário informa e-mail e senha. Após autenticação, o sistema redireciona para o painel administrativo.

### 5.6 Dashboard

O dashboard apresenta indicadores gerais e atalhos para os painéis dos módulos do sistema. A navegação foi reorganizada conforme o benchmarking estudado, separando as áreas em Financeiro, Pessoas, Ministérios, Células, Comunicação, Intercessão e Configurações.

Cada painel de módulo apresenta cards de indicadores, atalhos para as principais ações e listas resumidas com dados recentes. Essa melhoria permite que o usuário comece pelo painel da área e depois acesse as telas de gerenciamento.

### 5.7 Usuários

O módulo de usuários permite cadastrar novos acessos administrativos, definir perfil, informar senha provisória, listar usuários e aplicar exclusão lógica.

Esse módulo é separado do cadastro público. Pessoas que se cadastram pelo app entram como visitantes no módulo de Pessoas, sem permissão de acesso ao painel administrativo.

### 5.8 Membros e visitantes

O módulo permite cadastrar pessoas, classificar como membro ou visitante, editar dados, vincular ministérios e células, registrar histórico espiritual e aplicar inativação ou exclusão lógica. O painel de pessoas também exibe cadastros recentes, indicadores e aniversariantes do mês.

### 5.9 Famílias

O usuário pode cadastrar famílias, definir responsável e vincular membros cadastrados.

### 5.10 Ministérios

O usuário pode acessar o painel de ministérios, cadastrar ministérios, informar líder, dia de reunião, vagas e acompanhar participantes.

### 5.11 Células

O usuário pode acessar o painel de células, cadastrar células com líder, bairro, endereço, dia e horário de reunião, além de acompanhar presenças vinculadas.

### 5.12 Presença

O usuário pode registrar presença por data, tipo de encontro e membro vinculado.

### 5.13 Eventos

O usuário administrativo pode cadastrar eventos com nome, descrição, data, local, status e banner. Eventos não cancelados também ficam disponíveis na agenda do app do usuário.

### 5.14 Financeiro

O usuário pode acessar o painel financeiro, consultar receitas, despesas, doações, movimentações e cadastros auxiliares. Também pode consultar categorias, centro de custos, contas bancárias, formas de recebimento e formas de pagamento. Para cadastrar uma entrada ou saída, informa categoria, conta, membro ou fornecedor, valor e data.

### 5.15 Fornecedores

O usuário pode cadastrar fornecedores para vincular aos gastos registrados no módulo financeiro.

### 5.16 Doações

O usuário administrativo pode registrar doações, definir status, forma de recebimento, recorrência simples e baixar doações pendentes para o financeiro. No app do usuário, a tela de doações exibe apenas informações de contribuição configuradas pela administração.

### 5.17 Comunicação

O usuário administrativo pode acessar o painel de comunicação, acompanhar feed/mural, cadastrar comunicados, selecionar canal, destino, assunto, corpo e status. O item devocional reaproveita o mural para publicações internas e também aparece no app do usuário quando publicado.

### 5.18 Mural

O usuário pode cadastrar avisos, enviar imagem, publicar ou arquivar comunicados. Avisos publicados aparecem no feed do app do usuário.

### 5.19 Intercessão

O usuário administrativo pode acessar o painel de intercessão, registrar pedidos de oração, marcar que orou, indicar que o pedido foi respondido, arquivar e consultar testemunhos a partir dos pedidos respondidos. Pedidos enviados pelo app do usuário entram neste mesmo módulo.

### 5.20 Relatórios

O usuário pode visualizar indicadores operacionais e exportar os dados em Excel ou PDF, além de imprimir pelo navegador.

### 5.21 Configurações

O usuário pode alterar dados da igreja, parâmetros administrativos, informações do app do usuário e registrar backup lógico. O menu de configurações também possui páginas específicas para igreja, história, informações, programação, permissões de acesso, app e módulos ativos.

### 5.22 Testes

Para executar os testes:

```powershell
python -m unittest discover -s tests -q
```

## 6. CONSIDERAÇÕES FINAIS

O Sistema de Membresia Church atende ao objetivo de centralizar os principais processos administrativos de uma igreja em uma aplicação web. O projeto evoluiu de uma estrutura inicial com telas básicas para uma aplicação com banco MySQL real, módulos organizados, ações administrativas, relatórios, validações e uma frente pública em formato de app web para o usuário final.

A utilização de Flask, Jinja2, Bootstrap e MySQL permitiu aplicar os conteúdos trabalhados na disciplina de Programação para Internet de forma prática. O projeto também respeita a estrutura padrão ensinada nas aulas, com separação entre rotas, templates, arquivos estáticos, scripts de banco e testes.

O estudo de sistemas similares, registrado no benchmarking visual, também contribuiu para orientar a evolução da aplicação. A partir dele, foram identificadas melhorias como painéis por módulo, reorganização do menu por áreas, relatórios específicos, aniversários, testemunhos, devocional, centro de custos, formas de pagamento, formas de recebimento, configurações mais detalhadas da igreja e a separação entre painel administrativo e app do usuário.

Como evoluções futuras, podem ser adicionadas permissões mais detalhadas por perfil, envio real de mensagens, integração com e-mail, dashboards gráficos, controle de backups automatizados, deploy em ambiente de produção, notificações para o app do usuário e as melhorias planejadas a partir do benchmarking.

## REFERÊNCIAS

GTI-Fatec-Jahu. Programacao_Internet-GTI. Material de aulas da disciplina de Programação para Internet. Disponível em: https://github.com/GTI-Fatec-Jahu/Programacao_Internet-GTI.

PALLETS PROJECTS. Flask Documentation. Disponível em: https://flask.palletsprojects.com/.

PALLETS PROJECTS. Jinja Documentation. Disponível em: https://jinja.palletsprojects.com/.

ORACLE. MySQL Documentation. Disponível em: https://dev.mysql.com/doc/.

ORACLE. MySQL Connector/Python Developer Guide. Disponível em: https://dev.mysql.com/doc/connector-python/en/.

BOOTSTRAP TEAM. Bootstrap Documentation. Disponível em: https://getbootstrap.com/.

PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponível em: https://docs.python.org/.

PYTHON SOFTWARE FOUNDATION. unittest - Unit testing framework. Disponível em: https://docs.python.org/3/library/unittest.html.

MOZILLA DEVELOPER NETWORK. HTTP request methods. Disponível em: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods.

GOOGLE CLOUD. What is vibe coding? Disponível em: https://cloud.google.com/discover/what-is-vibe-coding.

TLDRAW. Domus Control - Benchmarking Sistemas. Quadro colaborativo de estudo visual. Disponível em: https://www.tldraw.com/f/fuyUxwevcohnMqp_YVxJU.
