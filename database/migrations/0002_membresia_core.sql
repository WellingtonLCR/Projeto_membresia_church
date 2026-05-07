BEGIN;

CREATE TABLE IF NOT EXISTS ministerios (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(100) UNIQUE NOT NULL,
  lider VARCHAR(120) NOT NULL,
  dia_reuniao VARCHAR(20) NOT NULL,
  vagas INTEGER NOT NULL DEFAULT 0 CHECK (vagas >= 0),
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
  atualizado_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS membros (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  telefone VARCHAR(30) NOT NULL,
  ministerio_id BIGINT REFERENCES ministerios(id) ON DELETE SET NULL,
  situacao VARCHAR(20) NOT NULL DEFAULT 'Ativo',
  observacoes TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
  atualizado_em TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_membros_nome ON membros(nome);
CREATE INDEX IF NOT EXISTS idx_membros_situacao ON membros(situacao);
CREATE INDEX IF NOT EXISTS idx_membros_ministerio ON membros(ministerio_id);

COMMIT;
