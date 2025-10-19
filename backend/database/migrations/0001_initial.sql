-- Таблица игроков
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    coins INTEGER DEFAULT 0,
    damage INTEGER DEFAULT 1,
    dragon_type TEXT DEFAULT 'fire',
    last_active TIMESTAMP,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица драконов
CREATE TABLE IF NOT EXISTS dragons (
    dragon_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    base_damage INTEGER NOT NULL,
    ability TEXT NOT NULL,
    price INTEGER NOT NULL
);

-- Таблица бустов
CREATE TABLE IF NOT EXISTS boosts (
    boost_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    effect TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price INTEGER NOT NULL
);

-- Таблица активных бустов игроков
CREATE TABLE IF NOT EXISTS player_boosts (
    user_id INTEGER,
    boost_id TEXT,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES players (user_id),
    FOREIGN KEY (boost_id) REFERENCES boosts (boost_id),
    PRIMARY KEY (user_id, boost_id)
);

ALTER TABLE players 
ADD COLUMN referrer_id INTEGER DEFAULT NULL;

ALTER TABLE players
ADD COLUMN referrals_count INTEGER DEFAULT 0;

ALTER TABLE players
ADD COLUMN is_banned BOOLEAN DEFAULT FALSE;

CREATE INDEX idx_referrer ON players(referrer_id);