# Sistema de Membresia Church

CENTRO PAULA SOUZA  
FACULDADE DE TECNOLOGIA DE JAHU  
CURSO DE TECNOLOGIA EM SISTEMAS PARA INTERNET

Wellington Luis Costa Ribeiro

Sistema de Membresia Church

Jau, SP  
2026

## AGRADECIMENTOS

Agradecemos a Faculdade de Tecnologia de Jahu pela estrutura academica e pelo ambiente de aprendizado oferecido durante o desenvolvimento deste projeto.

Agradeco ao Prof. Ronan Adriel Zenatti, orientador deste projeto, pelo material de aula, pelas orientacoes sobre Flask, Jinja2, MySQL, CRUD, templates, rotas e organizacao de projeto, que serviram como base para a construcao deste sistema.

Agradeco tambem aos colegas de curso pelas trocas de conhecimento, revisoes e sugestoes feitas durante a evolucao da aplicacao.

## RESUMO

O presente projeto tem como objetivo o desenvolvimento de um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e banco de dados MySQL. A aplicacao foi criada para centralizar cadastros e processos administrativos que normalmente ficam espalhados em planilhas, controles manuais ou registros informais, dificultando a organizacao e a consulta das informacoes.

O sistema permite o gerenciamento de membros, visitantes, familias, ministerios, celulas, presencas, eventos, financeiro, fornecedores, doacoes, comunicacao, mural, pedidos de oracao, relatorios, usuarios e configuracoes. A persistencia dos dados e realizada em banco MySQL real, conforme o conteudo trabalhado nas aulas, sem uso de listas em memoria para os dados principais do projeto.

Durante o desenvolvimento foram aplicados conceitos de rotas publicas e privadas, formularios com metodos GET e POST, heranca de templates, mensagens de retorno com flash, SQL parametrizado, exclusao logica, validacoes de formulario e organizacao por templates de entidade. O resultado e uma aplicacao funcional, estruturada e alinhada aos requisitos academicos da disciplina.

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
Figura 4. Pagina inicial do sistema.  
Figura 5. Pagina de login.  
Figura 6. Dashboard administrativo.  
Figura 7. Pagina de membros.  
Figura 8. Pagina de ministerios.  
Figura 9. Pagina de celulas.  
Figura 10. Pagina de eventos.  
Figura 11. Pagina financeira.  
Figura 12. Pagina de comunicacao.  
Figura 13. Pagina de relatorios.  
Figura 14. Pagina de configuracoes.  
Figura 15. Pagina da equipe.

## SUMARIO

1. INTRODUCAO  
1.1 PROBLEMATIZACAO  
1.2 Objetivo geral  
1.3 Objetivos especificos  
1.4 METODOLOGIA DA PESQUISA  
1.5 ESTRUTURA DO TRABALHO  
2. REVISAO BIBLIOGRAFICA  
2.1 SISTEMAS WEB PARA GESTAO ADMINISTRATIVA  
2.2 PERSISTENCIA DE DADOS COM MYSQL  
2.3 USABILIDADE E ORGANIZACAO DA INFORMACAO  
3. MODELO DE NEGOCIOS  
3.1 CANVAS  
3.2 O QUE SERA ELABORADO  
3.3 PARA QUEM SERA ELABORADO  
3.4 COMO SERA ELABORADO  
3.5 QUANTO CUSTARA  
4. DOCUMENTACAO  
4.1 DECLARACAO DE ABRANGENCIA DO PROJETO  
4.2 Requisitos funcionais  
4.3 Requisitos nao funcionais  
4.4 Casos de uso  
4.5 Modelo conceitual  
5. MANUAL DO USUARIO  
6. CONSIDERACOES FINAIS  
REFERENCIAS

## 1. INTRODUCAO

Igrejas e organizacoes religiosas lidam diariamente com informacoes de membros, visitantes, ministerios, celulas, eventos, contribuicoes financeiras, presencas e comunicacoes internas. Quando esses dados sao controlados de forma manual ou descentralizada, a gestao se torna mais lenta, sujeita a erros e dificil de acompanhar.

O Sistema de Membresia Church foi desenvolvido como uma aplicacao web para auxiliar a administracao de uma igreja local. A proposta e reunir em uma unica plataforma os principais cadastros e controles necessarios para a secretaria, lideranca, ministerios e equipe administrativa.

O projeto utiliza Flask como framework web, Jinja2 para templates HTML, Bootstrap para interface responsiva e MySQL para armazenamento permanente dos dados. A aplicacao segue os padroes trabalhados nas aulas de Programacao para Internet, especialmente a organizacao de rotas, templates, formularios, conexao com banco de dados e operacoes CRUD.

### 1.1 PROBLEMATIZACAO

O controle de membresia pode se tornar complexo quando a igreja cresce e passa a lidar com grande volume de informacoes. Cadastros duplicados, ausencia de historico, dificuldade para localizar dados, falta de controle de presenca, registros financeiros separados e comunicacao desorganizada sao problemas comuns.

Diante desse contexto, surge a seguinte questao: como desenvolver um sistema web simples, organizado e funcional que permita centralizar os principais processos administrativos de uma igreja, respeitando os conteudos e requisitos da disciplina?

### 1.2 Objetivo geral

Desenvolver um sistema web de membresia para igrejas, utilizando Python, Flask, Jinja2, Bootstrap e MySQL, com funcionalidades de cadastro, consulta, organizacao administrativa e relatorios.

### 1.3 Objetivos especificos

- Criar uma aplicacao Flask com rotas publicas e rotas protegidas por login.
- Utilizar templates Jinja2 com heranca por `base.html` e `base_publica.html`.
- Implementar formularios com validacao no back-end.
- Persistir os dados principais em banco MySQL real.
- Criar operacoes de cadastro, listagem, edicao, exclusao logica e acoes administrativas.
- Organizar os templates por entidade, conforme a estrutura ensinada nas aulas.
- Desenvolver uma interface responsiva com Bootstrap e CSS proprio.
- Implementar relatorios com opcoes de exportacao e impressao.
- Registrar testes automatizados para validar rotas e comportamentos principais.

### 1.4 METODOLOGIA DA PESQUISA

O desenvolvimento foi conduzido a partir da analise do material de aula da disciplina de Programacao para Internet, com foco nas aulas de Flask, Jinja2, formularios, conexao MySQL, CRUD, autenticacao, relatorios e organizacao de projeto.

Inicialmente, foi definida a estrutura base do sistema, contendo `app.py`, `db.py`, `db_setup.py`, `templates`, `static`, `database` e `tests`. Em seguida, foram modeladas as tabelas principais no MySQL, com scripts de migracao e seed para dados iniciais.

As funcionalidades foram implementadas por modulos, seguindo o fluxo:

- levantamento do caso de uso;
- criacao ou ajuste da tabela no banco;
- criacao da rota Flask;
- criacao do template Jinja2;
- validacao dos dados recebidos por formulario;
- persistencia no MySQL com SQL parametrizado;
- teste de renderizacao e comportamento.

Tambem foram analisados projetos de referencia em Laravel e Next.js para identificar funcionalidades que poderiam ser trazidas ao sistema sem fugir do escopo academico e sem alterar a arquitetura Flask do projeto.

### 1.5 ESTRUTURA DO TRABALHO

Este README foi organizado seguindo a estrutura do documento de referencia:

- O Capitulo 1 apresenta a introducao, problema, objetivos e metodologia.
- O Capitulo 2 apresenta a revisao bibliografica relacionada ao projeto.
- O Capitulo 3 descreve o modelo de negocios.
- O Capitulo 4 apresenta a documentacao tecnica e os requisitos.
- O Capitulo 5 apresenta o manual do usuario.
- O Capitulo 6 apresenta as consideracoes finais.

## 2. REVISAO BIBLIOGRAFICA

### 2.1 SISTEMAS WEB PARA GESTAO ADMINISTRATIVA

Sistemas web permitem que informacoes sejam acessadas por meio de navegador, sem necessidade de instalacao local em cada computador. Em contextos administrativos, esse modelo facilita o registro, consulta e atualizacao de dados, alem de favorecer a padronizacao dos processos.

No caso de uma igreja, um sistema web pode apoiar a secretaria e a lideranca no acompanhamento de membros, visitantes, ministerios, celulas, eventos e presencas. A centralizacao dessas informacoes reduz retrabalho e melhora a confiabilidade dos dados.

### 2.2 PERSISTENCIA DE DADOS COM MYSQL

O MySQL e um sistema gerenciador de banco de dados relacional utilizado para armazenar informacoes de forma persistente. Diferentemente de listas em memoria, os dados gravados no banco permanecem disponiveis mesmo apos reiniciar a aplicacao.

Neste projeto, a conexao com o MySQL foi centralizada em `db.py`, usando `mysql-connector-python`, pool de conexoes e queries parametrizadas com `%s`. Essa organizacao segue o material da disciplina e reduz repeticao de codigo nas rotas.

### 2.3 USABILIDADE E ORGANIZACAO DA INFORMACAO

A usabilidade e importante para que o usuario consiga localizar funcoes, preencher formularios e interpretar informacoes sem dificuldade. Por isso, o sistema utiliza menu lateral, cards de metricas, tabelas, botoes de acao, formularios com labels, mensagens de retorno e layout responsivo.

A organizacao dos templates por entidade tambem melhora a manutenibilidade do projeto, pois separa as telas de membros, ministerios, celulas, eventos, financeiro, comunicacao e demais modulos.

## 3. MODELO DE NEGOCIOS

### 3.1 CANVAS

O modelo Canvas foi usado como forma de organizar a proposta do sistema.

- Proposta de valor: centralizar a gestao administrativa e pastoral da igreja em uma unica aplicacao web.
- Segmento de usuarios: secretaria, administradores, lideres, pastores, equipe financeira e equipe de comunicacao.
- Canais: aplicacao web acessada pelo navegador em ambiente local.
- Relacionamento com usuarios: interface simples, mensagens de feedback, menu organizado e formularios objetivos.
- Atividades principais: cadastro, consulta, atualizacao, exclusao logica, relatorios e controle de processos internos.
- Recursos principais: computador, servidor Flask, banco MySQL, templates Jinja2, Bootstrap e codigo-fonte do projeto.
- Parcerias principais: Fatec Jahu, disciplina de Programacao para Internet e equipe de desenvolvimento.
- Estrutura de custos: desenvolvimento academico, infraestrutura local, computador, MySQL e manutencao futura.
- Fontes de receita: nao se aplica inicialmente, pois o projeto tem finalidade academica.

### 3.2 O QUE SERA ELABORADO

Sera elaborada uma aplicacao web de gestao de membresia para igrejas, com area publica, area administrativa protegida por login, modulos de cadastro, controles operacionais e relatorios.

### 3.3 PARA QUEM SERA ELABORADO

O sistema foi pensado para igrejas que precisam organizar informacoes de membros, visitantes, familias, ministerios, celulas, eventos, financeiro, comunicacao e acompanhamento pastoral.

Os principais usuarios sao:

- Administrador;
- Pastor;
- Secretaria;
- Lider;
- Financeiro.

### 3.4 COMO SERA ELABORADO

O sistema foi elaborado com Python e Flask no back-end, Jinja2 para renderizacao de templates, Bootstrap e CSS proprio na interface, MySQL para persistencia de dados e unittest para testes automatizados.

A estrutura segue o padrao:

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

Por ser um projeto academico, nao ha custo comercial inicial. O desenvolvimento foi realizado com ferramentas gratuitas e de codigo aberto. Em um ambiente real, poderiam existir custos com hospedagem, dominio, manutencao, backups e suporte tecnico.

## 4. DOCUMENTACAO

### 4.1 DECLARACAO DE ABRANGENCIA DO PROJETO

O projeto abrange o desenvolvimento de um sistema web para administracao de membresia de igreja, contemplando area publica, login, painel administrativo e modulos de gestao.

Estao dentro do escopo:

- cadastro e controle de usuarios;
- cadastro de membros e visitantes;
- familias e vinculo familiar;
- ministerios e celulas;
- presenca;
- eventos com banner;
- financeiro, fornecedores e doacoes;
- comunicacao, mural e intercessao;
- relatorios;
- configuracoes administrativas;
- persistencia em MySQL.

Nao fazem parte do escopo atual:

- integracao real com WhatsApp, e-mail externo ou gateway de pagamento;
- hospedagem em servidor de producao;
- aplicativo mobile nativo;
- controle avancado de permissoes por tela;
- envio automatico de notificacoes.

### 4.2 Requisitos funcionais

R1. O sistema deve permitir login e logout de usuarios administrativos.  
R2. O sistema deve permitir cadastro publico de usuario.  
R3. O sistema deve permitir recuperar senha de acesso.  
R4. O sistema deve permitir cadastrar usuarios com senha provisoria.  
R5. O sistema deve permitir listar, editar, bloquear, inativar e excluir logicamente usuarios.  
R6. O sistema deve permitir cadastrar, listar, editar, inativar e excluir logicamente membros.  
R7. O sistema deve permitir cadastrar e listar visitantes.  
R8. O sistema deve permitir registrar historico espiritual de membros.  
R9. O sistema deve permitir cadastrar familias e vincular membros a elas.  
R10. O sistema deve permitir cadastrar, listar, editar e excluir logicamente ministerios.  
R11. O sistema deve permitir cadastrar e listar celulas.  
R12. O sistema deve permitir registrar presenca por culto, evento ou celula.  
R13. O sistema deve permitir cadastrar e listar eventos com banner.  
R14. O sistema deve permitir cadastrar lancamentos financeiros de entrada e saida.  
R15. O sistema deve permitir cadastrar fornecedores e vincula-los a gastos.  
R16. O sistema deve permitir cadastrar doacoes e baixar doacoes pendentes para o financeiro.  
R17. O sistema deve permitir cadastrar mensagens de comunicacao.  
R18. O sistema deve permitir cadastrar, publicar e arquivar avisos no mural.  
R19. O sistema deve permitir cadastrar pedidos de oracao, registrar oracao, marcar como respondido e arquivar.  
R20. O sistema deve permitir consultar relatorios e exportar em Excel ou PDF.  
R21. O sistema deve permitir editar configuracoes administrativas da igreja.

### 4.3 Requisitos nao funcionais

RNF1. O sistema deve utilizar banco de dados MySQL real.  
RNF2. O sistema deve utilizar SQL parametrizado para reduzir risco de SQL Injection.  
RNF3. O sistema deve possuir interface responsiva com Bootstrap.  
RNF4. O sistema deve organizar templates com heranca Jinja2.  
RNF5. O sistema deve usar rotas protegidas para area administrativa.  
RNF6. O sistema deve exibir mensagens de retorno para acoes do usuario.  
RNF7. O sistema deve manter arquivos estaticos em `static` e templates em `templates`.  
RNF8. O sistema deve possuir `.gitignore` para evitar versionamento de cache, ambiente virtual e uploads dinamicos.  
RNF9. O sistema deve ter testes automatizados basicos.  
RNF10. O sistema deve ser simples de executar em ambiente local.

### 4.4 Casos de uso

Visitante publico

- acessar pagina inicial;
- acessar login;
- acessar cadastro;
- acessar recuperacao de senha;
- visualizar pagina da equipe.

Administrador

- acessar dashboard;
- gerenciar usuarios;
- gerenciar membros e visitantes;
- gerenciar familias;
- gerenciar ministerios;
- gerenciar celulas;
- gerenciar eventos;
- registrar presencas;
- gerenciar financeiro;
- gerenciar fornecedores;
- gerenciar doacoes;
- gerenciar comunicacao;
- gerenciar mural;
- acompanhar intercessao;
- consultar relatorios;
- alterar configuracoes.

Financeiro

- cadastrar entrada;
- cadastrar saida;
- vincular fornecedor;
- registrar doacao;
- baixar doacao pendente;
- consultar saldo e movimentacoes.

Lider

- consultar membros;
- acompanhar celulas;
- registrar presenca;
- consultar eventos;
- acompanhar pedidos de oracao.

### 4.5 Modelo conceitual

O modelo conceitual do sistema contempla as seguintes entidades principais:

- Usuarios;
- Perfis;
- Igreja;
- Membros;
- Familias;
- Ministerios;
- Celulas;
- Presencas;
- Eventos;
- Inscricoes de eventos;
- Categorias financeiras;
- Contas financeiras;
- Lancamentos financeiros;
- Fornecedores;
- Doacoes;
- Mensagens;
- Mural de avisos;
- Pedidos de oracao;
- Configuracoes do sistema.

Principais relacionamentos:

- Um usuario possui perfil.
- Um membro pode estar vinculado a uma celula.
- Um membro pode participar de varios ministerios.
- Uma familia pode possuir varios membros.
- Um evento pode possuir inscricoes.
- Um lancamento financeiro pode estar vinculado a membro, conta, categoria e fornecedor.
- Uma doacao pode gerar lancamento financeiro.
- Uma mensagem pode ser enviada por usuario administrativo.
- Um aviso de mural pode ser criado por usuario administrativo.

## 5. MANUAL DO USUARIO

### 5.1 Preparacao do ambiente

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Configure o banco:

```powershell
python db_setup.py
```

Inicie a aplicacao:

```powershell
flask --app app run --debug
```

Acesse:

```text
http://127.0.0.1:5000
```

### 5.2 Usuario inicial

```text
E-mail: admin@igreja.org
Senha: admin123
```

### 5.3 Pagina inicial

A pagina inicial apresenta o sistema e permite que o usuario acesse login, cadastro e demais telas publicas.

### 5.4 Login

Na pagina de login, o usuario informa e-mail e senha. Apos autenticacao, o sistema redireciona para o painel administrativo.

### 5.5 Dashboard

O dashboard apresenta indicadores gerais e atalhos para os modulos do sistema.

### 5.6 Usuarios

O modulo de usuarios permite cadastrar novos acessos administrativos, definir perfil, informar senha provisoria, listar usuarios e aplicar exclusao logica.

### 5.7 Membros e visitantes

O modulo permite cadastrar pessoas, classificar como membro ou visitante, editar dados, vincular ministerios e celulas, registrar historico espiritual e aplicar inativacao ou exclusao logica.

### 5.8 Familias

O usuario pode cadastrar familias, definir responsavel e vincular membros cadastrados.

### 5.9 Ministerios

O usuario pode cadastrar ministerios, informar lider, dia de reuniao, vagas e acompanhar participantes.

### 5.10 Celulas

O usuario pode cadastrar celulas com lider, bairro, endereco, dia e horario de reuniao.

### 5.11 Presenca

O usuario pode registrar presenca por data, tipo de encontro e membro vinculado.

### 5.12 Eventos

O usuario pode cadastrar eventos com nome, descricao, data, local, status e banner.

### 5.13 Financeiro

O usuario pode cadastrar entradas e saidas, selecionar categoria, conta, membro, fornecedor, valor e data.

### 5.14 Fornecedores

O usuario pode cadastrar fornecedores para vincular aos gastos registrados no modulo financeiro.

### 5.15 Doacoes

O usuario pode registrar doacoes, definir status, forma de recebimento, recorrencia simples e baixar doacoes pendentes para o financeiro.

### 5.16 Comunicacao

O usuario pode cadastrar mensagens, selecionar canal, destino, assunto, corpo e status.

### 5.17 Mural

O usuario pode cadastrar avisos, enviar imagem, publicar ou arquivar comunicados.

### 5.18 Intercessao

O usuario pode registrar pedidos de oracao, marcar que orou, indicar que o pedido foi respondido ou arquivar.

### 5.19 Relatorios

O usuario pode visualizar indicadores operacionais e exportar os dados em Excel ou PDF, alem de imprimir pelo navegador.

### 5.20 Configuracoes

O usuario pode alterar dados da igreja, parametros administrativos e registrar backup logico.

### 5.21 Testes

Para executar os testes:

```powershell
python -m unittest discover -s tests -q
```

## 6. CONSIDERACOES FINAIS

O Sistema de Membresia Church atende ao objetivo de centralizar os principais processos administrativos de uma igreja em uma aplicacao web. O projeto evoluiu de uma estrutura inicial com telas basicas para uma aplicacao com banco MySQL real, modulos organizados, acoes administrativas, relatorios e validacoes.

A utilizacao de Flask, Jinja2, Bootstrap e MySQL permitiu aplicar os conteudos trabalhados na disciplina de Programacao para Internet de forma pratica. O projeto tambem respeita a estrutura padrao ensinada nas aulas, com separacao entre rotas, templates, arquivos estaticos, scripts de banco e testes.

Como evolucoes futuras, podem ser adicionadas permissoes mais detalhadas por perfil, envio real de mensagens, integracao com e-mail, dashboards graficos, controle de backups automatizados e deploy em ambiente de producao.

## REFERENCIAS

GTI-Fatec-Jahu. Programacao_Internet-GTI. Material de aulas da disciplina de Programacao para Internet. Disponivel em: https://github.com/GTI-Fatec-Jahu/Programacao_Internet-GTI.

PALLETS PROJECTS. Flask Documentation. Disponivel em: https://flask.palletsprojects.com/.

PALLETS PROJECTS. Jinja Documentation. Disponivel em: https://jinja.palletsprojects.com/.

ORACLE. MySQL Documentation. Disponivel em: https://dev.mysql.com/doc/.

BOOTSTRAP TEAM. Bootstrap Documentation. Disponivel em: https://getbootstrap.com/.

PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponivel em: https://docs.python.org/.
