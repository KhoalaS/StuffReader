CREATE TABLE IF NOT EXISTS cookies (handle TEXT, key TEXT, value TEXT);
CREATE TABLE IF NOT EXISTS gallery_state (
    handle TEXT,
    id TEXT,
    completed INTEGER,
    bookmarked INTEGER,
    last_page INTEGER
);