-- ============================================================
-- Migration: 001_create_tables
-- Database: PostgreSQL
-- ============================================================

CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fields (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL UNIQUE,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS models (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    provider   VARCHAR(100) NOT NULL,
    version    VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS prompts (
    id            SERIAL PRIMARY KEY,
    version       VARCHAR(20) NOT NULL,
    system_prompt TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS main (
    id                SERIAL PRIMARY KEY,
    username          VARCHAR(100) NOT NULL,
    title             VARCHAR(200) NOT NULL,
    abstract          TEXT NOT NULL,
    university        VARCHAR(200) NOT NULL,
    table_of_contents TEXT NOT NULL,
    author            VARCHAR(200) NOT NULL,
    supervisor        VARCHAR(200) NOT NULL,
    field_id          INTEGER REFERENCES fields(id),
    category_id       INTEGER REFERENCES categories(id),
    model_id          INTEGER REFERENCES models(id),
    prompt_id         INTEGER REFERENCES prompts(id),
    status            VARCHAR(50) NOT NULL DEFAULT 'ready',
    output_json       JSONB,
    error_message     TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_main_status         ON main(status);
CREATE INDEX IF NOT EXISTS idx_main_status_created ON main(status, created_at);
CREATE INDEX IF NOT EXISTS idx_main_category       ON main(category_id);
CREATE INDEX IF NOT EXISTS idx_main_field          ON main(field_id);