BEGIN;

INSERT INTO perfis (nome, descricao)
VALUES
  ('ADMINISTRADOR', 'Acesso completo ao sistema de membresia'),
  ('SECRETARIA', 'Gestao de cadastros de membros e visitantes'),
  ('PASTORAL', 'Acompanhamento pastoral de membros e ministerios'),
  ('TESOURARIA', 'Consulta administrativa de membros para apoio operacional'),
  ('VOLUNTARIO', 'Consulta limitada de membros e ministerios')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO permissoes (modulo, acao, codigo, descricao)
VALUES
  ('MEMBROS', 'VIEW', 'membros.view', 'Visualizar membros cadastrados'),
  ('MEMBROS', 'CREATE', 'membros.create', 'Cadastrar novos membros'),
  ('MEMBROS', 'EDIT', 'membros.edit', 'Editar dados de membros'),
  ('MEMBROS', 'DELETE', 'membros.delete', 'Remover membros'),

  ('MINISTERIOS', 'VIEW', 'ministerios.view', 'Visualizar ministerios'),
  ('MINISTERIOS', 'CREATE', 'ministerios.create', 'Cadastrar ministerios'),
  ('MINISTERIOS', 'EDIT', 'ministerios.edit', 'Editar ministerios'),
  ('MINISTERIOS', 'DELETE', 'ministerios.delete', 'Remover ministerios'),

  ('USUARIOS', 'VIEW', 'usuarios.view', 'Visualizar usuarios do sistema'),
  ('USUARIOS', 'CREATE', 'usuarios.create', 'Cadastrar usuarios administrativos'),
  ('USUARIOS', 'EDIT', 'usuarios.edit', 'Editar usuarios administrativos'),
  ('USUARIOS', 'DELETE', 'usuarios.delete', 'Remover usuarios administrativos')
ON CONFLICT (codigo) DO NOTHING;

WITH perfil_admin AS (
  SELECT id FROM perfis WHERE nome = 'ADMINISTRADOR'
), todas_permissoes AS (
  SELECT id FROM permissoes
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_admin.id, todas_permissoes.id
FROM perfil_admin, todas_permissoes
ON CONFLICT DO NOTHING;

WITH perfil_secretaria AS (
  SELECT id FROM perfis WHERE nome = 'SECRETARIA'
), permissoes_secretaria AS (
  SELECT id FROM permissoes WHERE codigo IN (
    'membros.view', 'membros.create', 'membros.edit',
    'ministerios.view',
    'usuarios.view'
  )
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_secretaria.id, permissoes_secretaria.id
FROM perfil_secretaria, permissoes_secretaria
ON CONFLICT DO NOTHING;

WITH perfil_pastoral AS (
  SELECT id FROM perfis WHERE nome = 'PASTORAL'
), permissoes_pastoral AS (
  SELECT id FROM permissoes WHERE codigo IN (
    'membros.view', 'membros.edit',
    'ministerios.view', 'ministerios.create', 'ministerios.edit'
  )
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_pastoral.id, permissoes_pastoral.id
FROM perfil_pastoral, permissoes_pastoral
ON CONFLICT DO NOTHING;

WITH perfil_tesouraria AS (
  SELECT id FROM perfis WHERE nome = 'TESOURARIA'
), permissoes_tesouraria AS (
  SELECT id FROM permissoes WHERE codigo IN ('membros.view', 'ministerios.view')
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_tesouraria.id, permissoes_tesouraria.id
FROM perfil_tesouraria, permissoes_tesouraria
ON CONFLICT DO NOTHING;

WITH perfil_voluntario AS (
  SELECT id FROM perfis WHERE nome = 'VOLUNTARIO'
), permissoes_voluntario AS (
  SELECT id FROM permissoes WHERE codigo IN ('membros.view', 'ministerios.view')
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_voluntario.id, permissoes_voluntario.id
FROM perfil_voluntario, permissoes_voluntario
ON CONFLICT DO NOTHING;

COMMIT;
