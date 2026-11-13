-- =============================================================================
-- GymManager — Migração V001: criação do esquema inicial
-- IC: GYM-DB-001 · Responsável: DBA/DevOps (João Vitor Simonetti)
-- Modelo de referência: documentos/arquitetura/Modelo_de_Dados.md (GYM-ARQ-002)
--
-- REGRA (RNF11): migração já aplicada NUNCA é editada. Correções entram como
-- nova migração V<NNN>__<descricao>.sql. O executor confere o checksum.
-- =============================================================================

-- Usuários do sistema: administradores, instrutores e alunos (RF01, RF02, RF06)
CREATE TABLE usuario (
    id               INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    nome             VARCHAR(100)     NOT NULL,
    email            VARCHAR(254)     NOT NULL,
    senha_hash       VARCHAR(255)     NOT NULL,
    perfil           ENUM('ADMIN', 'INSTRUTOR', 'ALUNO') NOT NULL,
    ativo            TINYINT(1)       NOT NULL DEFAULT 1,
    data_nascimento  DATE             NULL,
    telefone         VARCHAR(20)      NULL,
    criado_em        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_usuario PRIMARY KEY (id),
    CONSTRAINT uq_usuario_email UNIQUE (email),
    INDEX ix_usuario_perfil_ativo (perfil, ativo)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Sessões de acesso: guarda apenas o hash SHA-256 do token (RF02, RNF01)
CREATE TABLE sessao (
    id          INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    usuario_id  INT UNSIGNED  NOT NULL,
    token_hash  CHAR(64)      NOT NULL,
    criado_em   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expira_em   DATETIME      NOT NULL,
    CONSTRAINT pk_sessao PRIMARY KEY (id),
    CONSTRAINT uq_sessao_token UNIQUE (token_hash),
    CONSTRAINT fk_sessao_usuario FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE,
    INDEX ix_sessao_expira (expira_em)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Catálogo de exercícios (RF03). Nunca excluído, apenas inativado (RN04)
CREATE TABLE exercicio (
    id              INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nome            VARCHAR(100)  NOT NULL,
    grupo_muscular  VARCHAR(50)   NULL,
    descricao       TEXT          NULL,
    ativo           TINYINT(1)    NOT NULL DEFAULT 1,
    criado_em       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_exercicio PRIMARY KEY (id),
    CONSTRAINT uq_exercicio_nome UNIQUE (nome),
    INDEX ix_exercicio_grupo (grupo_muscular)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Ficha de treino: pertence a um único aluno (RN06), criada por instrutor/admin (RN01)
CREATE TABLE ficha (
    id             INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nome           VARCHAR(100)  NOT NULL,
    aluno_id       INT UNSIGNED  NOT NULL,
    instrutor_id   INT UNSIGNED  NOT NULL,
    data_inicio    DATE          NOT NULL,
    data_fim       DATE          NULL,
    ativa          TINYINT(1)    NOT NULL DEFAULT 1,
    criado_em      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_ficha PRIMARY KEY (id),
    CONSTRAINT fk_ficha_aluno FOREIGN KEY (aluno_id) REFERENCES usuario (id),
    CONSTRAINT fk_ficha_instrutor FOREIGN KEY (instrutor_id) REFERENCES usuario (id),
    CONSTRAINT ck_ficha_datas CHECK (data_fim IS NULL OR data_fim >= data_inicio),
    INDEX ix_ficha_aluno_ativa (aluno_id, ativa)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Itens da ficha: exercício + séries, repetições, carga e descanso (RF04)
CREATE TABLE ficha_exercicio (
    id            INT UNSIGNED       NOT NULL AUTO_INCREMENT,
    ficha_id      INT UNSIGNED       NOT NULL,
    exercicio_id  INT UNSIGNED       NOT NULL,
    series        SMALLINT UNSIGNED  NOT NULL,
    repeticoes    SMALLINT UNSIGNED  NOT NULL,
    carga_kg      DECIMAL(6, 2)      NOT NULL DEFAULT 0.00,
    descanso_s    SMALLINT UNSIGNED  NOT NULL DEFAULT 0,
    ordem         SMALLINT UNSIGNED  NOT NULL DEFAULT 1,
    ativo         TINYINT(1)         NOT NULL DEFAULT 1,
    CONSTRAINT pk_ficha_exercicio PRIMARY KEY (id),
    CONSTRAINT fk_fe_ficha FOREIGN KEY (ficha_id) REFERENCES ficha (id),
    CONSTRAINT fk_fe_exercicio FOREIGN KEY (exercicio_id) REFERENCES exercicio (id),
    CONSTRAINT ck_fe_series CHECK (series > 0),
    CONSTRAINT ck_fe_repeticoes CHECK (repeticoes > 0),
    CONSTRAINT ck_fe_carga CHECK (carga_kg >= 0),
    INDEX ix_fe_ficha_ordem (ficha_id, ativo, ordem)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Execução de treino: sessão em que o aluno realizou a ficha (RF05, RN07)
CREATE TABLE execucao (
    id        INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    ficha_id  INT UNSIGNED  NOT NULL,
    aluno_id  INT UNSIGNED  NOT NULL,
    inicio    DATETIME      NOT NULL,
    fim       DATETIME      NULL,
    CONSTRAINT pk_execucao PRIMARY KEY (id),
    CONSTRAINT fk_execucao_ficha FOREIGN KEY (ficha_id) REFERENCES ficha (id),
    CONSTRAINT fk_execucao_aluno FOREIGN KEY (aluno_id) REFERENCES usuario (id),
    CONSTRAINT ck_execucao_datas CHECK (fim IS NULL OR fim >= inicio),
    INDEX ix_execucao_aluno_inicio (aluno_id, inicio)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Registro de cada exercício executado: repetições e carga realizadas (RF05)
CREATE TABLE execucao_exercicio (
    id                  INT UNSIGNED       NOT NULL AUTO_INCREMENT,
    execucao_id         INT UNSIGNED       NOT NULL,
    ficha_exercicio_id  INT UNSIGNED       NOT NULL,
    repeticoes          SMALLINT UNSIGNED  NOT NULL,
    carga_kg            DECIMAL(6, 2)      NOT NULL DEFAULT 0.00,
    registrado_em       DATETIME           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_execucao_exercicio PRIMARY KEY (id),
    CONSTRAINT uq_ee_execucao_item UNIQUE (execucao_id, ficha_exercicio_id),
    CONSTRAINT fk_ee_execucao FOREIGN KEY (execucao_id) REFERENCES execucao (id),
    CONSTRAINT fk_ee_ficha_exercicio FOREIGN KEY (ficha_exercicio_id) REFERENCES ficha_exercicio (id),
    CONSTRAINT ck_ee_repeticoes CHECK (repeticoes > 0),
    CONSTRAINT ck_ee_carga CHECK (carga_kg >= 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
