START TRANSACTION;

INSERT INTO configuracoes_sistema (chave, valor, descricao)
VALUES
  ('igreja.nome', 'Igreja Viva', 'Nome exibido no sistema'),
  ('igreja.email', 'contato@igrejaviva.org', 'E-mail institucional exibido nas configurações'),
  ('igreja.telefone', '(14) 3333-2026', 'Telefone institucional exibido nas configurações'),
  ('programacao.domingo', 'Domingo às 19h30 - Culto de celebração', 'Programação fixa de domingo exibida no app do usuário'),
  ('programacao.quarta', 'Quarta às 20h - Oração e ensino bíblico', 'Programação fixa de quarta exibida no app do usuário'),
  ('programacao.celulas', 'Terça a sexta, conforme o bairro da célula', 'Programação de células exibida no app do usuário'),
  ('doacao.pix', 'pix@igrejaviva.org', 'Chave PIX exibida no app do usuário'),
  ('doacao.banco', 'Banco 001 - Ag. 1234 - Conta 98765-0', 'Dados bancários exibidos no app do usuário'),
  ('doacao.mensagem', 'Sua contribuição apoia cultos, ações sociais, células e cuidado pastoral.', 'Mensagem de contribuição exibida no app do usuário')
ON DUPLICATE KEY UPDATE
  valor = VALUES(valor),
  descricao = VALUES(descricao);

INSERT INTO ministerios (nome, descricao, lider_nome, dia_reuniao, vagas, ativo)
SELECT 'Louvor', 'Equipe responsável pela música dos cultos e eventos.', 'Marina Duarte', 'Quinta', 8, 1
WHERE NOT EXISTS (SELECT 1 FROM ministerios WHERE nome = 'Louvor');

INSERT INTO ministerios (nome, descricao, lider_nome, dia_reuniao, vagas, ativo)
SELECT 'Intercessão', 'Equipe de acompanhamento dos pedidos de oração.', 'Paulo Mendes', 'Quarta', 12, 1
WHERE NOT EXISTS (SELECT 1 FROM ministerios WHERE nome = 'Intercessão');

INSERT INTO ministerios (nome, descricao, lider_nome, dia_reuniao, vagas, ativo)
SELECT 'Ação Social', 'Equipe responsável por campanhas e apoio comunitário.', 'Renata Alves', 'Sábado', 15, 1
WHERE NOT EXISTS (SELECT 1 FROM ministerios WHERE nome = 'Ação Social');

INSERT INTO ministerios (nome, descricao, lider_nome, dia_reuniao, vagas, ativo)
SELECT 'Kids', 'Cuidado e ensino das crianças durante os cultos.', 'Fernanda Lima', 'Domingo', 10, 1
WHERE NOT EXISTS (SELECT 1 FROM ministerios WHERE nome = 'Kids');

INSERT INTO celulas (nome, lider_nome, bairro, endereco, dia_reuniao, horario, ativo)
SELECT 'Célula Centro', 'Carlos Souza', 'Centro', 'Rua das Flores, 120', 'Terça', '20:00:00', 1
WHERE NOT EXISTS (SELECT 1 FROM celulas WHERE nome = 'Célula Centro');

INSERT INTO celulas (nome, lider_nome, bairro, endereco, dia_reuniao, horario, ativo)
SELECT 'Célula Jardim', 'Ana Souza', 'Jardim América', 'Av. Brasil, 450', 'Quinta', '20:00:00', 1
WHERE NOT EXISTS (SELECT 1 FROM celulas WHERE nome = 'Célula Jardim');

INSERT INTO celulas (nome, lider_nome, bairro, endereco, dia_reuniao, horario, ativo)
SELECT 'Célula Universitária', 'Lucas Martins', 'Vila Nova', 'Rua Projetada, 88', 'Sexta', '19:30:00', 1
WHERE NOT EXISTS (SELECT 1 FROM celulas WHERE nome = 'Célula Universitária');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Ana Souza', '1992-05-12', 'Rua das Flores, 120', '(14) 99991-1001', '(14) 99991-1001', 'ana.souza@igreja.org', 'Casado(a)', 'Professora', DATE_SUB(CURDATE(), INTERVAL 620 DAY), (SELECT id FROM celulas WHERE nome = 'Célula Jardim' LIMIT 1), 'Vocal', 'Ativo', 'Cadastro demo para apresentação do sistema.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'ana.souza@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Carlos Souza', '1988-09-21', 'Rua das Flores, 120', '(14) 99991-1002', '(14) 99991-1002', 'carlos.souza@igreja.org', 'Casado(a)', 'Analista', DATE_SUB(CURDATE(), INTERVAL 620 DAY), (SELECT id FROM celulas WHERE nome = 'Célula Centro' LIMIT 1), 'Líder de célula', 'Ativo', 'Cadastro demo para apresentação do sistema.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'carlos.souza@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Marina Duarte', '1995-03-08', 'Av. Brasil, 450', '(14) 99991-1003', '(14) 99991-1003', 'marina.duarte@igreja.org', 'Solteiro(a)', 'Música', DATE_SUB(CURDATE(), INTERVAL 420 DAY), (SELECT id FROM celulas WHERE nome = 'Célula Centro' LIMIT 1), 'Líder de louvor', 'Ativo', 'Cadastro demo para apresentação do sistema.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'marina.duarte@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'João Pedro Lima', '2001-11-18', 'Rua Projetada, 88', '(14) 99991-1004', '(14) 99991-1004', 'joao.lima@exemplo.com', 'Solteiro(a)', 'Estudante', CURDATE(), (SELECT id FROM celulas WHERE nome = 'Célula Universitária' LIMIT 1), NULL, 'Visitante', 'Visitante cadastrado como exemplo do app do usuário.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'joao.lima@exemplo.com');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Beatriz Nunes', '1999-02-02', 'Rua Esperança, 32', '(14) 99991-1005', '(14) 99991-1005', 'beatriz.nunes@exemplo.com', 'Solteiro(a)', 'Designer', CURDATE(), NULL, NULL, 'Visitante', 'Visitante cadastrada como exemplo do app do usuário.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'beatriz.nunes@exemplo.com');

INSERT INTO familias (nome, responsavel_membro_id, telefone, endereco, observacoes, ativo)
SELECT 'Família Souza', (SELECT id FROM membros WHERE email = 'carlos.souza@igreja.org' LIMIT 1), '(14) 99991-1002', 'Rua das Flores, 120', 'Família demo vinculada a membros ativos.', 1
WHERE NOT EXISTS (SELECT 1 FROM familias WHERE nome = 'Família Souza');

INSERT IGNORE INTO familia_membros (familia_id, membro_id, parentesco)
SELECT f.id, m.id, 'Responsável'
FROM familias f
JOIN membros m ON m.email = 'carlos.souza@igreja.org'
WHERE f.nome = 'Família Souza';

INSERT IGNORE INTO familia_membros (familia_id, membro_id, parentesco)
SELECT f.id, m.id, 'Cônjuge'
FROM familias f
JOIN membros m ON m.email = 'ana.souza@igreja.org'
WHERE f.nome = 'Família Souza';

INSERT IGNORE INTO membro_ministerio (membro_id, ministerio_id, funcao, ativo, entrada_em)
SELECT m.id, mi.id, 'Vocal', 1, DATE_SUB(CURDATE(), INTERVAL 360 DAY)
FROM membros m
JOIN ministerios mi ON mi.nome = 'Louvor'
WHERE m.email = 'ana.souza@igreja.org';

INSERT IGNORE INTO membro_ministerio (membro_id, ministerio_id, funcao, ativo, entrada_em)
SELECT m.id, mi.id, 'Líder', 1, DATE_SUB(CURDATE(), INTERVAL 360 DAY)
FROM membros m
JOIN ministerios mi ON mi.nome = 'Louvor'
WHERE m.email = 'marina.duarte@igreja.org';

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Culto de Celebração', 'Culto principal com louvor, palavra e momento de comunhão.', DATE_ADD(NOW(), INTERVAL 3 DAY), DATE_ADD(DATE_ADD(NOW(), INTERVAL 3 DAY), INTERVAL 2 HOUR), 'Templo principal', 'Agendado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Culto de Celebração');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Encontro de Células', 'Noite de integração entre células, visitantes e liderança.', DATE_ADD(NOW(), INTERVAL 7 DAY), DATE_ADD(DATE_ADD(NOW(), INTERVAL 7 DAY), INTERVAL 2 HOUR), 'Salão social', 'Agendado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Encontro de Células');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Campanha Ação Social', 'Arrecadação de alimentos e roupas para famílias atendidas.', DATE_ADD(NOW(), INTERVAL 14 DAY), DATE_ADD(DATE_ADD(NOW(), INTERVAL 14 DAY), INTERVAL 4 HOUR), 'Pátio da igreja', 'Agendado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Campanha Ação Social');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id)
SELECT 'Bem-vindos ao app da Igreja Viva', 'Comunicado', 'Acompanhe por aqui os avisos, eventos e cuidados publicados pela equipe administrativa.', 'Publicado', NOW(), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Bem-vindos ao app da Igreja Viva');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id)
SELECT 'Devocional da semana', 'Devocional', 'Permaneçam firmes na esperança, servindo com alegria e cuidando uns dos outros em amor.', 'Publicado', NOW(), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Devocional da semana');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id)
SELECT 'Escala de voluntários', 'Aviso', 'As equipes de recepção, louvor e kids já podem consultar a escala do próximo culto.', 'Publicado', NOW(), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Escala de voluntários');

INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, status, privado, oracoes)
SELECT 'João Pedro Lima', '(14) 99991-1004', 'Vida espiritual', 'Pedido de direção e fortalecimento na caminhada cristã.', 'Pendente', 1, 3
WHERE NOT EXISTS (SELECT 1 FROM pedidos_oracao WHERE solicitante_nome = 'João Pedro Lima' AND pedido LIKE 'Pedido de direção%');

INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, status, privado, oracoes)
SELECT 'Beatriz Nunes', '(14) 99991-1005', 'Trabalho', 'Agradecimento por uma nova oportunidade profissional recebida nesta semana.', 'Respondido', 0, 12
WHERE NOT EXISTS (SELECT 1 FROM pedidos_oracao WHERE solicitante_nome = 'Beatriz Nunes' AND status = 'Respondido');

INSERT INTO fornecedores (nome, documento, telefone, email, endereco, observacoes, ativo)
SELECT 'Mercado Solidário', '12.345.678/0001-90', '(14) 3333-1000', 'contato@mercadosolidario.com', 'Av. Central, 200', 'Fornecedor demo para despesas de ação social.', 1
WHERE NOT EXISTS (SELECT 1 FROM fornecedores WHERE nome = 'Mercado Solidário');

INSERT INTO doacoes (membro_id, doador_nome, tipo, categoria_id, conta_id, valor, data_doacao, forma_recebimento, recorrente, status, observacoes)
SELECT (SELECT id FROM membros WHERE email = 'ana.souza@igreja.org' LIMIT 1), 'Ana Souza', 'Dizimo', (SELECT id FROM categorias_financeiras WHERE nome = 'Dizimo' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), 350.00, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'PIX', 1, 'Recebida', 'Doação demo vinculada a membro.'
WHERE NOT EXISTS (SELECT 1 FROM doacoes WHERE doador_nome = 'Ana Souza' AND valor = 350.00);

INSERT INTO doacoes (membro_id, doador_nome, tipo, categoria_id, conta_id, valor, data_doacao, forma_recebimento, recorrente, status, observacoes)
SELECT NULL, 'Visitante anônimo', 'Oferta', (SELECT id FROM categorias_financeiras WHERE nome = 'Oferta' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), 120.00, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Dinheiro', 0, 'Recebida', 'Oferta demo sem membro vinculado.'
WHERE NOT EXISTS (SELECT 1 FROM doacoes WHERE doador_nome = 'Visitante anônimo' AND valor = 120.00);

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Entrada', (SELECT id FROM categorias_financeiras WHERE nome = 'Oferta' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), NULL, NULL, 'Oferta culto de celebração - demo', 120.00, DATE_SUB(CURDATE(), INTERVAL 2 DAY), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Oferta culto de celebração - demo');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Saida', (SELECT id FROM categorias_financeiras WHERE nome = 'Material de consumo' AND tipo = 'Saida' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), NULL, (SELECT id FROM fornecedores WHERE nome = 'Mercado Solidário' LIMIT 1), 'Materiais para ação social - demo', 280.00, DATE_SUB(CURDATE(), INTERVAL 1 DAY), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Materiais para ação social - demo');

INSERT INTO mensagens (canal, assunto, corpo, destino_tipo, status, agendada_para, enviada_em, criado_por_usuario_id)
SELECT 'Interna', 'Boas-vindas aos visitantes', 'Mensagem demo para acompanhamento dos visitantes cadastrados pelo app.', 'Geral', 'Enviada', NULL, NOW(), (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM mensagens WHERE assunto = 'Boas-vindas aos visitantes');

COMMIT;
