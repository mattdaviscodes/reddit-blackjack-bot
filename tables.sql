-- Player-specific data
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    credits DEFAULT 500,
    is_blocked INTEGER DEFAULT 0, -- 0 or 1. Flag to allow manual ban of annoying players
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);

-- Track the achievements earned by players
CREATE TABLE IF NOT EXISTS player_achievements (
    player_achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    achievement_type_id INTEGER NOT NULL,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (achievement_type_id) REFERENCES achievement_types(achievement_type_id)
);

-- High level game data
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP),
    completed_date TEXT,    -- NULL indicates incomplete game
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Full game state after every interaction (enables hand history)
CREATE TABLE IF NOT EXISTS game_states (
    game_state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    pickled_game TEXT,
    reated_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);

-- Commands will be identified by one process and stored here. Commands are only
-- evaluated for syntatic validity, not game state permission. Responses and
-- permission evaluation will be handled by a separate process.
CREATE TABLE IF NOT EXISTS commands (
    command_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    command_type_id INTEGER NOT NULL,
    full_text TEXT NOT NULL,    -- Original fulltext in case a comment is edited
    permalink TEXT NOT NULL,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP), -- Actually 'found_date', keeping 'created' for consistent naming
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (command_type_id) REFERENCES command_types(command_type_id)
);

-- All responses to commands by bot. If a command doesn't have an associated
-- action, then that command has not yet been responded to.
CREATE TABLE IF NOT EXISTS actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_id INTEGER NOT NULL,
    action_type_id INTEGER NOT NULL,
    FOREIGN KEY (command_id) REFERENCES commands(command_id),
    FOREIGN KEY (action_type_id) REFERENCES action_types(action_type_id)
);

-- Record all credit exchanges between bot and players
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id INTEGER NOT NULL,
    credit_change INTEGER NOT NULL,
    FOREIGN KEY (action_id) REFERENCES actions(action_id)
);




/* ========== META REDDIT TABLES ========== */

-- MAGIC NUMBER: -1 for direct messages
CREATE TABLE IF NOT EXISTS posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subreddit_id INTEGER NOT NULL,
    title TEXT,
    FOREIGN KEY (subreddit_id) REFERENCES subreddits(subreddit_id)
);

-- All subreddits that players have been active in
-- MAGIC NUMBER: -1 for direct messages
CREATE TABLE IF NOT EXISTS subreddits (
    subreddit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_is_banned INTEGER, -- 1 or 0, true if bot has been banned by sub's mods
    is_blocked INTEGER DEFAULT 0, -- 1 or 0, true if manual block for annoying subs in place :-)
    over_18 INTEGER,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);




/* ========== LOOKUP TABLES ========== */

-- Lookup table for all allowed commands (i.e. Hit, Stay, Highscores, etc)
CREATE TABLE IF NOT EXISTS command_types (
    command_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);

-- Lookup table for all allowed action types (i.e. Hit, recharge credits,
-- new player, etc). This is different than comand_types. Commands are things a
-- player told the bot to do, and they all map to comments. Actions are things
-- that the bot actually did. The actions table will server as a much better log
-- of all activity than the commands.
-- MAGIC NUMBER: -1 for disallowed command
CREATE TABLE IF NOT EXISTS action_types (
    action_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);

-- Lookup table for all player achievements
CREATE TABLE IF NOT EXISTS achievement_types (
    achievement_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    created_date TEXT DEFAULT (CURRENT_TIMESTAMP)
);

/* SNIPPETS


CREATE TABLE IF NOT EXISTS (
     INTEGER PRIMARY KEY AUTOINCREMENT,
);


created_date TEXT DEFAULT (CURRENT_TIMESTAMP)


*/
