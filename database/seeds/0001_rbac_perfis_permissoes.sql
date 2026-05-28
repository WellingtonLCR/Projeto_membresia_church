START TRANSACTION;

INSERT IGNORE INTO perfis (nome, descricao)
VALUES
  ('ADMINISTRADOR', 'Acesso completo ao sistema de membresia'),
  ('PASTOR', 'Acompanhamento pastoral, espiritual e eclesiástico'),
  ('SECRETARIA', 'Gestão de cadastros, presença, eventos e relatórios administrativos'),
  ('LIDER', 'Consulta e acompanhamento de ministérios e células vinculadas'),
  ('FINANCEIRO', 'Gestão de entradas, saídas, dízimos, ofertas e relatórios financeiros');

INSERT IGNORE INTO permissoes (modulo, acao, codigo, descricao)
VALUES
  ('DASHBOARD', 'VIEW', 'dashboard.view', 'Visualizar dashboard'),
  ('MEMBROS', 'VIEW', 'membros.view', 'Visualizar membros'),
  ('MEMBROS', 'CREATE', 'membros.create', 'Cadastrar membros e visitantes'),
  ('MEMBROS', 'EDIT', 'membros.edit', 'Editar dados pessoais e eclesiásticos'),
  ('MEMBROS', 'DELETE', 'membros.delete', 'Executar exclusão lógica de membros'),
  ('MEMBROS', 'PASTORAL', 'membros.pastoral', 'Registrar histórico espiritual e acompanhamento pastoral'),
  ('MINISTERIOS', 'VIEW', 'ministerios.view', 'Visualizar ministérios'),
  ('MINISTERIOS', 'CREATE', 'ministerios.create', 'Cadastrar ministérios'),
  ('MINISTERIOS', 'EDIT', 'ministerios.edit', 'Editar ministérios e participantes'),
  ('MINISTERIOS', 'DELETE', 'ministerios.delete', 'Inativar ministérios'),
  ('CELULAS', 'VIEW', 'celulas.view', 'Visualizar células'),
  ('CELULAS', 'CREATE', 'celulas.create', 'Cadastrar células'),
  ('CELULAS', 'EDIT', 'celulas.edit', 'Editar células, reuniões e presença'),
  ('PRESENCA', 'VIEW', 'presenca.view', 'Visualizar presença'),
  ('PRESENCA', 'CREATE', 'presenca.create', 'Registrar presença'),
  ('EVENTOS', 'VIEW', 'eventos.view', 'Visualizar eventos'),
  ('EVENTOS', 'CREATE', 'eventos.create', 'Cadastrar eventos'),
  ('EVENTOS', 'EDIT', 'eventos.edit', 'Editar eventos e inscrições'),
  ('FINANCEIRO', 'VIEW', 'financeiro.view', 'Visualizar financeiro'),
  ('FINANCEIRO', 'CREATE', 'financeiro.create', 'Cadastrar entradas e saídas'),
  ('FINANCEIRO', 'EDIT', 'financeiro.edit', 'Editar lançamentos financeiros'),
  ('FINANCEIRO', 'EXPORT', 'financeiro.export', 'Exportar relatórios financeiros'),
  ('COMUNICACAO', 'VIEW', 'comunicacao.view', 'Visualizar comunicação'),
  ('COMUNICACAO', 'SEND', 'comunicacao.send', 'Enviar WhatsApp, e-mail e notificações internas'),
  ('RELATORIOS', 'VIEW', 'relatorios.view', 'Visualizar relatórios'),
  ('RELATORIOS', 'EXPORT', 'relatorios.export', 'Exportar relatórios em PDF ou Excel'),
  ('USUARIOS', 'VIEW', 'usuarios.view', 'Visualizar usuários'),
  ('USUARIOS', 'CREATE', 'usuarios.create', 'Cadastrar usuários'),
  ('USUARIOS', 'EDIT', 'usuarios.edit', 'Editar usuários, perfis e bloqueios'),
  ('CONFIGURACOES', 'MANAGE', 'configuracoes.manage', 'Gerenciar configurações gerais, permissões e backups');

INSERT IGNORE INTO perfil_permissao (perfil_id, permissao_id)
SELECT p.id, perm.id
FROM perfis p
JOIN permissoes perm ON 1 = 1
WHERE p.nome = 'ADMINISTRADOR';

INSERT IGNORE INTO perfil_permissao (perfil_id, permissao_id)
SELECT p.id, perm.id
FROM perfis p
JOIN permissoes perm ON perm.codigo IN (
  'dashboard.view', 'membros.view', 'membros.edit', 'membros.pastoral',
  'ministerios.view', 'celulas.view', 'presenca.view', 'eventos.view',
  'comunicacao.view', 'relatorios.view'
)
WHERE p.nome = 'PASTOR';

INSERT IGNORE INTO perfil_permissao (perfil_id, permissao_id)
SELECT p.id, perm.id
FROM perfis p
JOIN permissoes perm ON perm.codigo IN (
  'dashboard.view', 'membros.view', 'membros.create', 'membros.edit',
  'ministerios.view', 'celulas.view', 'presenca.view', 'presenca.create',
  'eventos.view', 'eventos.create', 'eventos.edit',
  'comunicacao.view', 'comunicacao.send', 'relatorios.view', 'relatorios.export'
)
WHERE p.nome = 'SECRETARIA';

INSERT IGNORE INTO perfil_permissao (perfil_id, permissao_id)
SELECT p.id, perm.id
FROM perfis p
JOIN permissoes perm ON perm.codigo IN (
  'dashboard.view', 'membros.view', 'ministerios.view', 'ministerios.edit',
  'celulas.view', 'celulas.edit', 'presenca.view', 'presenca.create',
  'eventos.view', 'comunicacao.view'
)
WHERE p.nome = 'LIDER';

INSERT IGNORE INTO perfil_permissao (perfil_id, permissao_id)
SELECT p.id, perm.id
FROM perfis p
JOIN permissoes perm ON perm.codigo IN (
  'dashboard.view', 'membros.view', 'financeiro.view', 'financeiro.create',
  'financeiro.edit', 'financeiro.export', 'relatorios.view', 'relatorios.export'
)
WHERE p.nome = 'FINANCEIRO';

INSERT IGNORE INTO configuracoes_sistema (chave, valor, descricao)
VALUES
  ('igreja.nome', 'Igreja Viva', 'Nome exibido no sistema'),
  ('backup.agendamento', 'Diário às 02:00', 'Rotina recomendada de backup do banco MySQL'),
  ('frequencia.baixa.percentual', '50', 'Percentual mínimo de presença mensal antes de alerta'),
  ('paginacao.tamanho_padrao', '20', 'Quantidade padrão de registros por página');

INSERT IGNORE INTO usuarios (nome, email, senha_hash, ativo, bloqueado)
VALUES (
  'Administrador Igreja Viva',
  'admin@igreja.org',
  'scrypt:32768:8:1$QjlGjHTL3kypUIAE$d2f8abe5c73fe8f6f866543494b73b0cf327788aadcd551b4a3557e60947e043ae56cde65941ecc7f00006e64d5e8948fcabf8be6cd7c154cb1eb86d565cec90',
  1,
  0
);

INSERT IGNORE INTO usuario_perfil (usuario_id, perfil_id)
SELECT u.id, p.id
FROM usuarios u
JOIN perfis p ON p.nome = 'ADMINISTRADOR'
WHERE u.email = 'admin@igreja.org';

INSERT IGNORE INTO igrejas (nome, email, telefone, endereco, logo_path)
VALUES ('Igreja Viva', NULL, NULL, NULL, 'static/imgs/logo_church.png');

INSERT IGNORE INTO categorias_financeiras (nome, tipo)
VALUES
  ('Dizimo', 'Entrada'),
  ('Oferta', 'Entrada'),
  ('Contribuicao', 'Entrada'),
  ('Manutencao', 'Saida'),
  ('Agua e luz', 'Saida'),
  ('Material de consumo', 'Saida');

INSERT IGNORE INTO contas_financeiras (nome, banco, saldo_inicial)
VALUES ('Conta principal', NULL, 0);

COMMIT;
