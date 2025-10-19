ALTER TABLE players 
ADD COLUMN referrer_id INTEGER DEFAULT NULL;

ALTER TABLE players
ADD COLUMN referrals_count INTEGER DEFAULT 0;

ALTER TABLE players
ADD COLUMN is_banned BOOLEAN DEFAULT FALSE;

CREATE INDEX idx_referrer ON players(referrer_id);