-- Создаем таблицу драконов
CREATE TABLE IF NOT EXISTS dragons (
    id TEXT PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    attack INTEGER DEFAULT 10,
    defense INTEGER DEFAULT 5,
    health INTEGER DEFAULT 100,
    experience INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES players (user_id)
);

-- Добавляем столбец active_dragon_id в players
ALTER TABLE players ADD COLUMN active_dragon_id TEXT;

-- Создаем индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_dragons_owner_id ON dragons(owner_id);
CREATE INDEX IF NOT EXISTS idx_dragons_type ON dragons(type);