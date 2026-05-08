START TRANSACTION;

CREATE TABLE IF NOT EXISTS perfis (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(60) NOT NULL UNIQUE,
  descricao TEXT,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuarios (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  senha_hash VARCHAR(255) NOT NULL,
  ativo TINYINT(1) NOT NULL DEFAULT 1,
  bloqueado TINYINT(1) NOT NULL DEFAULT 0,
  ultimo_login_em DATETIME NULL,
  excluido_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_usuarios_email (email),
  INDEX idx_usuarios_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS permissoes (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  modulo VARCHAR(60) NOT NULL,
  acao VARCHAR(30) NOT NULL,
  codigo VARCHAR(120) NOT NULL UNIQUE,
  descricao TEXT,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_permissoes_modulo (modulo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuario_perfil (
  usuario_id BIGINT UNSIGNED NOT NULL,
  perfil_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (usuario_id, perfil_id),
  CONSTRAINT fk_usuario_perfil_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  CONSTRAINT fk_usuario_perfil_perfil FOREIGN KEY (perfil_id) REFERENCES perfis(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS perfil_permissao (
  perfil_id BIGINT UNSIGNED NOT NULL,
  permissao_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (perfil_id, permissao_id),
  CONSTRAINT fk_perfil_permissao_perfil FOREIGN KEY (perfil_id) REFERENCES perfis(id) ON DELETE CASCADE,
  CONSTRAINT fk_perfil_permissao_permissao FOREIGN KEY (permissao_id) REFERENCES permissoes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuario_permissao (
  usuario_id BIGINT UNSIGNED NOT NULL,
  permissao_id BIGINT UNSIGNED NOT NULL,
  permitido TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (usuario_id, permissao_id),
  CONSTRAINT fk_usuario_permissao_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  CONSTRAINT fk_usuario_permissao_permissao FOREIGN KEY (permissao_id) REFERENCES permissoes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS auditoria_logs (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id BIGINT UNSIGNED NULL,
  modulo VARCHAR(60) NOT NULL,
  acao VARCHAR(30) NOT NULL,
  entidade VARCHAR(80) NOT NULL,
  entidade_id BIGINT UNSIGNED NULL,
  payload JSON NULL,
  ip_origem VARCHAR(45) NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_auditoria_usuario (usuario_id),
  INDEX idx_auditoria_modulo (modulo),
  INDEX idx_auditoria_entidade (entidade, entidade_id),
  CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;
