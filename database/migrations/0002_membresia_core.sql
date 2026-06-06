START TRANSACTION;

CREATE TABLE IF NOT EXISTS igrejas (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  documento VARCHAR(30) NULL,
  email VARCHAR(120) NULL,
  telefone VARCHAR(30) NULL,
  endereco TEXT NULL,
  logo_path VARCHAR(255) NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ministerios (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL UNIQUE,
  descricao TEXT NULL,
  lider_membro_id BIGINT UNSIGNED NULL,
  lider_nome VARCHAR(120) NULL,
  dia_reuniao VARCHAR(20) NULL,
  vagas INT NOT NULL DEFAULT 0,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_ministerios_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS celulas (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  lider_membro_id BIGINT UNSIGNED NULL,
  lider_nome VARCHAR(120) NULL,
  bairro VARCHAR(100) NULL,
  endereco TEXT NULL,
  dia_reuniao VARCHAR(20) NULL,
  horario TIME NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_celulas_ativo (ativo),
  INDEX idx_celulas_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS membros (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  cpf VARCHAR(20) NULL UNIQUE,
  data_nascimento DATE NULL,
  endereco TEXT NULL,
  telefone VARCHAR(30) NULL,
  whatsapp VARCHAR(30) NULL,
  email VARCHAR(120) NULL,
  estado_civil VARCHAR(30) NULL,
  profissao VARCHAR(120) NULL,
  data_entrada DATE NULL,
  data_batismo DATE NULL,
  celula_id BIGINT UNSIGNED NULL,
  cargo_funcao VARCHAR(120) NULL,
  status ENUM('Ativo', 'Inativo', 'Visitante', 'Afastado') NOT NULL DEFAULT 'Ativo',
  observacoes TEXT NULL,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_membros_nome (nome),
  INDEX idx_membros_status (status),
  INDEX idx_membros_email (email),
  INDEX idx_membros_telefone (telefone),
  INDEX idx_membros_celula (celula_id),
  CONSTRAINT fk_membros_celula FOREIGN KEY (celula_id) REFERENCES celulas(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS familias (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  responsavel_membro_id BIGINT UNSIGNED NULL,
  telefone VARCHAR(30) NULL,
  endereco TEXT NULL,
  observacoes TEXT NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_familias_nome (nome),
  INDEX idx_familias_ativo (ativo),
  CONSTRAINT fk_familias_responsavel FOREIGN KEY (responsavel_membro_id) REFERENCES membros(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS familia_membros (
  familia_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NOT NULL,
  parentesco VARCHAR(60) NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (familia_id, membro_id),
  CONSTRAINT fk_familia_membros_familia FOREIGN KEY (familia_id) REFERENCES familias(id) ON DELETE CASCADE,
  CONSTRAINT fk_familia_membros_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS membro_ministerio (
  membro_id BIGINT UNSIGNED NOT NULL,
  ministerio_id BIGINT UNSIGNED NOT NULL,
  funcao VARCHAR(120) NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  entrada_em DATE NULL,
  saida_em DATE NULL,
  PRIMARY KEY (membro_id, ministerio_id),
  CONSTRAINT fk_membro_ministerio_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE CASCADE,
  CONSTRAINT fk_membro_ministerio_ministerio FOREIGN KEY (ministerio_id) REFERENCES ministerios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS historico_espiritual (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  membro_id BIGINT UNSIGNED NOT NULL,
  tipo VARCHAR(80) NOT NULL,
  data_registro DATE NOT NULL,
  descricao TEXT NOT NULL,
  responsavel_usuario_id BIGINT UNSIGNED NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_historico_membro (membro_id),
  INDEX idx_historico_tipo (tipo),
  CONSTRAINT fk_historico_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE CASCADE,
  CONSTRAINT fk_historico_usuario FOREIGN KEY (responsavel_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS celula_reunioes (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  celula_id BIGINT UNSIGNED NOT NULL,
  data_reuniao DATE NOT NULL,
  tema VARCHAR(150) NULL,
  observacoes TEXT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_celula_reunioes_data (data_reuniao),
  CONSTRAINT fk_celula_reunioes_celula FOREIGN KEY (celula_id) REFERENCES celulas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS celula_presencas (
  reuniao_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NOT NULL,
  presente TINYINT(1) NOT NULL DEFAULT 1,
  visitante_nome VARCHAR(120) NULL,
  PRIMARY KEY (reuniao_id, membro_id),
  CONSTRAINT fk_celula_presencas_reuniao FOREIGN KEY (reuniao_id) REFERENCES celula_reunioes(id) ON DELETE CASCADE,
  CONSTRAINT fk_celula_presencas_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS eventos (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  descricao TEXT NULL,
  data_inicio DATETIME NOT NULL,
  data_fim DATETIME NULL,
  local VARCHAR(150) NULL,
  banner_path VARCHAR(255) NULL,
  status ENUM('Agendado', 'Realizado', 'Cancelado') NOT NULL DEFAULT 'Agendado',
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_eventos_data (data_inicio),
  INDEX idx_eventos_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS evento_inscricoes (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  evento_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NULL,
  visitante_nome VARCHAR(120) NULL,
  visitante_contato VARCHAR(120) NULL,
  presente TINYINT(1) NOT NULL DEFAULT 0,
  inscrito_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_evento_inscricoes_evento (evento_id),
  CONSTRAINT fk_evento_inscricoes_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
  CONSTRAINT fk_evento_inscricoes_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS presencas (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  membro_id BIGINT UNSIGNED NULL,
  tipo ENUM('Culto', 'Evento', 'Celula') NOT NULL,
  referencia_id BIGINT UNSIGNED NULL,
  referencia_nome VARCHAR(150) NULL,
  data_presenca DATE NOT NULL,
  presente TINYINT(1) NOT NULL DEFAULT 1,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_presencas_data (data_presenca),
  INDEX idx_presencas_membro (membro_id),
  INDEX idx_presencas_tipo (tipo),
  CONSTRAINT fk_presencas_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fornecedores (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  documento VARCHAR(30) NULL,
  telefone VARCHAR(30) NULL,
  email VARCHAR(120) NULL,
  endereco TEXT NULL,
  observacoes TEXT NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_fornecedores_nome (nome),
  INDEX idx_fornecedores_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categorias_financeiras (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  tipo ENUM('Entrada', 'Saida') NOT NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_categoria_tipo (nome, tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contas_financeiras (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL UNIQUE,
  banco VARCHAR(100) NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  saldo_inicial DECIMAL(12,2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lancamentos_financeiros (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('Entrada', 'Saida') NOT NULL,
  categoria_id BIGINT UNSIGNED NOT NULL,
  conta_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NULL,
  fornecedor_id BIGINT UNSIGNED NULL,
  descricao VARCHAR(180) NULL,
  valor DECIMAL(12,2) NOT NULL,
  data_lancamento DATE NOT NULL,
  comprovante_path VARCHAR(255) NULL,
  criado_por_usuario_id BIGINT UNSIGNED NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_lancamentos_data (data_lancamento),
  INDEX idx_lancamentos_tipo (tipo),
  INDEX idx_lancamentos_membro (membro_id),
  INDEX idx_lancamentos_fornecedor (fornecedor_id),
  CONSTRAINT fk_lancamentos_categoria FOREIGN KEY (categoria_id) REFERENCES categorias_financeiras(id),
  CONSTRAINT fk_lancamentos_conta FOREIGN KEY (conta_id) REFERENCES contas_financeiras(id),
  CONSTRAINT fk_lancamentos_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL,
  CONSTRAINT fk_lancamentos_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id) ON DELETE SET NULL,
  CONSTRAINT fk_lancamentos_usuario FOREIGN KEY (criado_por_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
  CHECK (valor >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS doacoes (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  membro_id BIGINT UNSIGNED NULL,
  doador_nome VARCHAR(120) NULL,
  tipo VARCHAR(60) NOT NULL,
  categoria_id BIGINT UNSIGNED NULL,
  conta_id BIGINT UNSIGNED NOT NULL,
  lancamento_financeiro_id BIGINT UNSIGNED NULL,
  valor DECIMAL(12,2) NOT NULL,
  data_doacao DATE NOT NULL,
  forma_recebimento VARCHAR(60) NULL,
  recorrente TINYINT(1) NOT NULL DEFAULT 0,
  status ENUM('Recebida', 'Pendente', 'Cancelada') NOT NULL DEFAULT 'Recebida',
  observacoes TEXT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_doacoes_data (data_doacao),
  INDEX idx_doacoes_status (status),
  INDEX idx_doacoes_membro (membro_id),
  CONSTRAINT fk_doacoes_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL,
  CONSTRAINT fk_doacoes_categoria FOREIGN KEY (categoria_id) REFERENCES categorias_financeiras(id) ON DELETE SET NULL,
  CONSTRAINT fk_doacoes_conta FOREIGN KEY (conta_id) REFERENCES contas_financeiras(id),
  CONSTRAINT fk_doacoes_lancamento FOREIGN KEY (lancamento_financeiro_id) REFERENCES lancamentos_financeiros(id) ON DELETE SET NULL,
  CHECK (valor >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comunicacao_listas (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL UNIQUE,
  tipo VARCHAR(60) NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comunicacao_lista_membros (
  lista_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (lista_id, membro_id),
  CONSTRAINT fk_lista_membros_lista FOREIGN KEY (lista_id) REFERENCES comunicacao_listas(id) ON DELETE CASCADE,
  CONSTRAINT fk_lista_membros_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mensagens (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  canal ENUM('WhatsApp', 'Email', 'Interna') NOT NULL,
  assunto VARCHAR(150) NOT NULL,
  corpo TEXT NOT NULL,
  destino_tipo ENUM('Geral', 'Ministerio', 'Celula', 'Lista', 'Aniversariantes', 'Individual') NOT NULL,
  destino_referencia_id BIGINT UNSIGNED NULL,
  status ENUM('Rascunho', 'Agendada', 'Enviada', 'Falha') NOT NULL DEFAULT 'Rascunho',
  agendada_para DATETIME NULL,
  enviada_em DATETIME NULL,
  criado_por_usuario_id BIGINT UNSIGNED NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_mensagens_canal (canal),
  INDEX idx_mensagens_status (status),
  CONSTRAINT fk_mensagens_usuario FOREIGN KEY (criado_por_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mensagem_destinatarios (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  mensagem_id BIGINT UNSIGNED NOT NULL,
  membro_id BIGINT UNSIGNED NULL,
  contato VARCHAR(150) NULL,
  status ENUM('Pendente', 'Enviado', 'Falha') NOT NULL DEFAULT 'Pendente',
  enviado_em DATETIME NULL,
  INDEX idx_msg_destinatarios_mensagem (mensagem_id),
  INDEX idx_msg_destinatarios_membro (membro_id),
  CONSTRAINT fk_msg_destinatarios_mensagem FOREIGN KEY (mensagem_id) REFERENCES mensagens(id) ON DELETE CASCADE,
  CONSTRAINT fk_msg_destinatarios_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mural_avisos (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  categoria VARCHAR(80) NULL,
  conteudo TEXT NOT NULL,
  imagem_path VARCHAR(255) NULL,
  status ENUM('Rascunho', 'Publicado', 'Arquivado') NOT NULL DEFAULT 'Rascunho',
  publicado_em DATETIME NULL,
  criado_por_usuario_id BIGINT UNSIGNED NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_mural_status (status),
  INDEX idx_mural_publicado (publicado_em),
  CONSTRAINT fk_mural_usuario FOREIGN KEY (criado_por_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedidos_oracao (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  solicitante_nome VARCHAR(120) NOT NULL,
  contato VARCHAR(120) NULL,
  categoria VARCHAR(80) NULL,
  pedido TEXT NOT NULL,
  status ENUM('Pendente', 'Em oracao', 'Respondido', 'Arquivado') NOT NULL DEFAULT 'Pendente',
  privado TINYINT(1) NOT NULL DEFAULT 0,
  oracoes INT NOT NULL DEFAULT 0,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_pedidos_status (status),
  INDEX idx_pedidos_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedido_oracao_reacoes (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pedido_id BIGINT UNSIGNED NOT NULL,
  autor_nome VARCHAR(120) NOT NULL,
  contato VARCHAR(120) NULL,
  tipo ENUM('orando', 'amem', 'forca') NOT NULL DEFAULT 'orando',
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_reacoes_pedido (pedido_id),
  INDEX idx_reacoes_tipo (tipo),
  CONSTRAINT fk_reacoes_pedido_oracao FOREIGN KEY (pedido_id) REFERENCES pedidos_oracao(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedido_oracao_comentarios (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pedido_id BIGINT UNSIGNED NOT NULL,
  autor_nome VARCHAR(120) NOT NULL,
  contato VARCHAR(120) NULL,
  comentario TEXT NOT NULL,
  aprovado TINYINT(1) NOT NULL DEFAULT 1,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_comentarios_pedido (pedido_id),
  INDEX idx_comentarios_aprovado (aprovado),
  CONSTRAINT fk_comentarios_pedido_oracao FOREIGN KEY (pedido_id) REFERENCES pedidos_oracao(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS configuracoes_sistema (
  chave VARCHAR(120) PRIMARY KEY,
  valor TEXT NULL,
  descricao TEXT NULL,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;
