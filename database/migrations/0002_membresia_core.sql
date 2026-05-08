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
  tipo ENUM('Batismo', 'Conversao', 'Profissao de fe', 'Transferencia', 'Desligamento', 'Discipulado', 'Acompanhamento pastoral', 'Pedido de oracao', 'Testemunho', 'Aconselhamento', 'Observacao') NOT NULL,
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
  descricao VARCHAR(180) NULL,
  valor DECIMAL(12,2) NOT NULL,
  data_lancamento DATE NOT NULL,
  comprovante_path VARCHAR(255) NULL,
  criado_por_usuario_id BIGINT UNSIGNED NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_lancamentos_data (data_lancamento),
  INDEX idx_lancamentos_tipo (tipo),
  INDEX idx_lancamentos_membro (membro_id),
  CONSTRAINT fk_lancamentos_categoria FOREIGN KEY (categoria_id) REFERENCES categorias_financeiras(id),
  CONSTRAINT fk_lancamentos_conta FOREIGN KEY (conta_id) REFERENCES contas_financeiras(id),
  CONSTRAINT fk_lancamentos_membro FOREIGN KEY (membro_id) REFERENCES membros(id) ON DELETE SET NULL,
  CONSTRAINT fk_lancamentos_usuario FOREIGN KEY (criado_por_usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
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

CREATE TABLE IF NOT EXISTS configuracoes_sistema (
  chave VARCHAR(120) PRIMARY KEY,
  valor TEXT NULL,
  descricao TEXT NULL,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;
