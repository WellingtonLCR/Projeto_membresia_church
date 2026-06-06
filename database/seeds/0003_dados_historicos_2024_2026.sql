START TRANSACTION;

INSERT INTO fornecedores (nome, documento, telefone, email, endereco, observacoes, ativo)
SELECT 'Papelaria Central', '22.333.444/0001-10', '(14) 3333-2200', 'financeiro@papelariacentral.com', 'Rua Major Prado, 450', 'Fornecedor demo para materiais administrativos.', 1
WHERE NOT EXISTS (SELECT 1 FROM fornecedores WHERE nome = 'Papelaria Central');

INSERT INTO fornecedores (nome, documento, telefone, email, endereco, observacoes, ativo)
SELECT 'Som e Luz Eventos', '33.444.555/0001-20', '(14) 3333-3300', 'contato@someluzeventos.com', 'Av. Brasil, 910', 'Fornecedor demo para apoio técnico em eventos.', 1
WHERE NOT EXISTS (SELECT 1 FROM fornecedores WHERE nome = 'Som e Luz Eventos');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Visitante Demo', '1990-04-12', 'Rua Antônia Pires de Campos, 570', '(14) 99164-6300', '(14) 99164-6300', 'visitante@igreja.org', 'Solteiro(a)', 'Estudante', '2026-02-15', NULL, NULL, 'Visitante', 'Usuário visitante demo para apresentação do app.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'visitante@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Pedro Almeida', '1987-01-18', 'Rua das Palmeiras, 44', '(14) 99992-2001', '(14) 99992-2001', 'pedro.almeida@igreja.org', 'Casado(a)', 'Técnico de informática', '2024-02-11', (SELECT id FROM celulas WHERE nome = 'Célula Centro' LIMIT 1), 'Diácono', 'Ativo', 'Cadastro histórico demo 2024.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'pedro.almeida@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Juliana Rocha', '1994-07-22', 'Rua XV de Novembro, 80', '(14) 99992-2002', '(14) 99992-2002', 'juliana.rocha@igreja.org', 'Solteiro(a)', 'Enfermeira', '2024-08-04', (SELECT id FROM celulas WHERE nome = 'Célula Jardim' LIMIT 1), 'Recepção', 'Ativo', 'Cadastro histórico demo 2024.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'juliana.rocha@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Rafael Martins', '1982-12-03', 'Av. Netinho Prado, 210', '(14) 99992-2003', '(14) 99992-2003', 'rafael.martins@igreja.org', 'Casado(a)', 'Motorista', '2025-03-19', (SELECT id FROM celulas WHERE nome = 'Célula Universitária' LIMIT 1), NULL, 'Ativo', 'Cadastro histórico demo 2025.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'rafael.martins@igreja.org');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Camila Ferreira', '2000-10-09', 'Rua Santa Luzia, 32', '(14) 99992-2004', '(14) 99992-2004', 'camila.ferreira@exemplo.com', 'Solteiro(a)', 'Estudante', '2025-11-09', NULL, NULL, 'Visitante', 'Visitante histórico demo 2025.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'camila.ferreira@exemplo.com');

INSERT INTO membros (nome, data_nascimento, endereco, telefone, whatsapp, email, estado_civil, profissao, data_entrada, celula_id, cargo_funcao, status, observacoes)
SELECT 'Sérgio Batista', '1979-06-30', 'Rua Riachuelo, 77', '(14) 99992-2005', '(14) 99992-2005', 'sergio.batista@igreja.org', 'Casado(a)', 'Contador', '2026-01-07', (SELECT id FROM celulas WHERE nome = 'Célula Centro' LIMIT 1), 'Tesouraria', 'Ativo', 'Cadastro histórico demo 2026.'
WHERE NOT EXISTS (SELECT 1 FROM membros WHERE email = 'sergio.batista@igreja.org');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Conferência de Família 2024', 'Evento anual de ensino e cuidado familiar.', '2024-04-20 19:30:00', '2024-04-20 22:00:00', 'Templo principal', 'Realizado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Conferência de Família 2024');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Escola Bíblica de Férias 2024', 'Programação infantil e familiar.', '2024-07-13 14:00:00', '2024-07-13 18:00:00', 'Salão social', 'Realizado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Escola Bíblica de Férias 2024');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Retiro de Líderes 2025', 'Treinamento para líderes de ministérios e células.', '2025-03-15 08:00:00', '2025-03-15 17:00:00', 'Chácara Betel', 'Realizado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Retiro de Líderes 2025');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Noite de Comunhão 2025', 'Encontro com visitantes e novos membros.', '2025-09-06 19:00:00', '2025-09-06 21:30:00', 'Pátio da igreja', 'Realizado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Noite de Comunhão 2025');

INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status)
SELECT 'Treinamento de Voluntários 2026', 'Capacitação para equipes de recepção, kids e comunicação.', '2026-03-21 09:00:00', '2026-03-21 12:00:00', 'Sala multiuso', 'Realizado'
WHERE NOT EXISTS (SELECT 1 FROM eventos WHERE nome = 'Treinamento de Voluntários 2026');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id, criado_em)
SELECT 'Agenda de início de ano 2024', 'Comunicado', 'Confira cultos, células e programações especiais do primeiro trimestre.', 'Publicado', '2024-01-08 09:00:00', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1), '2024-01-08 09:00:00'
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Agenda de início de ano 2024');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id, criado_em)
SELECT 'Devocional: cuidado em comunidade', 'Devocional', 'Uma reflexão sobre caminhar junto, servir com constância e cuidar de pessoas.', 'Publicado', '2025-05-05 07:30:00', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1), '2025-05-05 07:30:00'
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Devocional: cuidado em comunidade');

INSERT INTO mural_avisos (titulo, categoria, conteudo, status, publicado_em, criado_por_usuario_id, criado_em)
SELECT 'Campanha de alimentos 2026', 'Ação Social', 'A igreja receberá alimentos não perecíveis durante os cultos de junho.', 'Publicado', '2026-06-01 08:00:00', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1), '2026-06-01 08:00:00'
WHERE NOT EXISTS (SELECT 1 FROM mural_avisos WHERE titulo = 'Campanha de alimentos 2026');

INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, status, privado, oracoes, criado_em)
SELECT 'Pedro Almeida', '(14) 99992-2001', 'Familia', 'Pedido por restauração e diálogo familiar.', 'Respondido', 0, 18, '2024-05-10 20:15:00'
WHERE NOT EXISTS (SELECT 1 FROM pedidos_oracao WHERE solicitante_nome = 'Pedro Almeida' AND criado_em = '2024-05-10 20:15:00');

INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, status, privado, oracoes, criado_em)
SELECT 'Juliana Rocha', '(14) 99992-2002', 'Saude', 'Acompanhamento por tratamento de saúde na família.', 'Respondido', 0, 24, '2025-02-18 10:30:00'
WHERE NOT EXISTS (SELECT 1 FROM pedidos_oracao WHERE solicitante_nome = 'Juliana Rocha' AND criado_em = '2025-02-18 10:30:00');

INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, status, privado, oracoes, criado_em)
SELECT 'Camila Ferreira', '(14) 99992-2004', 'Vida espiritual', 'Desejo de conhecer mais sobre fé e comunidade.', 'Pendente', 1, 5, '2026-04-03 18:45:00'
WHERE NOT EXISTS (SELECT 1 FROM pedidos_oracao WHERE solicitante_nome = 'Camila Ferreira' AND criado_em = '2026-04-03 18:45:00');

INSERT INTO pedido_oracao_reacoes (pedido_id, autor_nome, contato, tipo, criado_em)
SELECT p.id, 'Ana Souza', NULL, 'orando', '2025-02-19 09:00:00'
FROM pedidos_oracao p
WHERE p.solicitante_nome = 'Juliana Rocha'
  AND NOT EXISTS (SELECT 1 FROM pedido_oracao_reacoes r WHERE r.pedido_id = p.id AND r.autor_nome = 'Ana Souza');

INSERT INTO pedido_oracao_comentarios (pedido_id, autor_nome, contato, comentario, aprovado, criado_em)
SELECT p.id, 'Marina Duarte', NULL, 'Seguimos em oração e celebramos a resposta com você.', 1, '2025-02-20 12:30:00'
FROM pedidos_oracao p
WHERE p.solicitante_nome = 'Juliana Rocha'
  AND NOT EXISTS (SELECT 1 FROM pedido_oracao_comentarios c WHERE c.pedido_id = p.id AND c.autor_nome = 'Marina Duarte');

INSERT INTO doacoes (membro_id, doador_nome, tipo, categoria_id, conta_id, valor, data_doacao, forma_recebimento, recorrente, status, observacoes)
SELECT (SELECT id FROM membros WHERE email = 'pedro.almeida@igreja.org' LIMIT 1), 'Pedro Almeida', 'Dizimo', (SELECT id FROM categorias_financeiras WHERE nome = 'Dizimo' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), 410.00, '2024-03-10', 'PIX', 1, 'Recebida', 'Dado histórico demo 2024.'
WHERE NOT EXISTS (SELECT 1 FROM doacoes WHERE doador_nome = 'Pedro Almeida' AND data_doacao = '2024-03-10');

INSERT INTO doacoes (membro_id, doador_nome, tipo, categoria_id, conta_id, valor, data_doacao, forma_recebimento, recorrente, status, observacoes)
SELECT (SELECT id FROM membros WHERE email = 'juliana.rocha@igreja.org' LIMIT 1), 'Juliana Rocha', 'Oferta', (SELECT id FROM categorias_financeiras WHERE nome = 'Oferta' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), 95.00, '2025-05-18', 'Dinheiro', 0, 'Recebida', 'Dado histórico demo 2025.'
WHERE NOT EXISTS (SELECT 1 FROM doacoes WHERE doador_nome = 'Juliana Rocha' AND data_doacao = '2025-05-18');

INSERT INTO doacoes (membro_id, doador_nome, tipo, categoria_id, conta_id, valor, data_doacao, forma_recebimento, recorrente, status, observacoes)
SELECT (SELECT id FROM membros WHERE email = 'sergio.batista@igreja.org' LIMIT 1), 'Sérgio Batista', 'Contribuicao', (SELECT id FROM categorias_financeiras WHERE nome = 'Contribuicao' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), 280.00, '2026-02-22', 'Transferencia', 0, 'Recebida', 'Dado histórico demo 2026.'
WHERE NOT EXISTS (SELECT 1 FROM doacoes WHERE doador_nome = 'Sérgio Batista' AND data_doacao = '2026-02-22');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Entrada', (SELECT id FROM categorias_financeiras WHERE nome = 'Dizimo' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), (SELECT id FROM membros WHERE email = 'pedro.almeida@igreja.org' LIMIT 1), NULL, 'Dízimo histórico Pedro Almeida 2024', 410.00, '2024-03-10', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Dízimo histórico Pedro Almeida 2024');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Saida', (SELECT id FROM categorias_financeiras WHERE nome = 'Material de consumo' AND tipo = 'Saida' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), NULL, (SELECT id FROM fornecedores WHERE nome = 'Papelaria Central' LIMIT 1), 'Materiais secretaria 2024', 185.50, '2024-06-14', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Materiais secretaria 2024');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Entrada', (SELECT id FROM categorias_financeiras WHERE nome = 'Oferta' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), (SELECT id FROM membros WHERE email = 'juliana.rocha@igreja.org' LIMIT 1), NULL, 'Oferta histórica Juliana Rocha 2025', 95.00, '2025-05-18', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Oferta histórica Juliana Rocha 2025');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Saida', (SELECT id FROM categorias_financeiras WHERE nome = 'Manutencao' AND tipo = 'Saida' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), NULL, (SELECT id FROM fornecedores WHERE nome = 'Som e Luz Eventos' LIMIT 1), 'Apoio técnico evento 2025', 720.00, '2025-09-05', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Apoio técnico evento 2025');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Entrada', (SELECT id FROM categorias_financeiras WHERE nome = 'Contribuicao' AND tipo = 'Entrada' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), (SELECT id FROM membros WHERE email = 'sergio.batista@igreja.org' LIMIT 1), NULL, 'Contribuição histórica Sérgio Batista 2026', 280.00, '2026-02-22', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Contribuição histórica Sérgio Batista 2026');

INSERT INTO lancamentos_financeiros (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
SELECT 'Saida', (SELECT id FROM categorias_financeiras WHERE nome = 'Agua e luz' AND tipo = 'Saida' LIMIT 1), (SELECT id FROM contas_financeiras WHERE nome = 'Conta principal' LIMIT 1), NULL, NULL, 'Contas fixas fevereiro 2026', 390.45, '2026-02-28', (SELECT id FROM usuarios WHERE email = 'admin@igreja.org' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM lancamentos_financeiros WHERE descricao = 'Contas fixas fevereiro 2026');

INSERT INTO presencas (membro_id, tipo, referencia_nome, data_presenca, presente)
SELECT id, 'Culto', 'Culto de celebração', '2024-04-21', 1 FROM membros WHERE email = 'pedro.almeida@igreja.org'
  AND NOT EXISTS (SELECT 1 FROM presencas WHERE referencia_nome = 'Culto de celebração' AND data_presenca = '2024-04-21' AND membro_id = membros.id);

INSERT INTO presencas (membro_id, tipo, referencia_nome, data_presenca, presente)
SELECT id, 'Celula', 'Célula Jardim', '2025-05-22', 1 FROM membros WHERE email = 'juliana.rocha@igreja.org'
  AND NOT EXISTS (SELECT 1 FROM presencas WHERE referencia_nome = 'Célula Jardim' AND data_presenca = '2025-05-22' AND membro_id = membros.id);

INSERT INTO presencas (membro_id, tipo, referencia_nome, data_presenca, presente)
SELECT id, 'Evento', 'Treinamento de Voluntários 2026', '2026-03-21', 1 FROM membros WHERE email = 'sergio.batista@igreja.org'
  AND NOT EXISTS (SELECT 1 FROM presencas WHERE referencia_nome = 'Treinamento de Voluntários 2026' AND data_presenca = '2026-03-21' AND membro_id = membros.id);

COMMIT;
