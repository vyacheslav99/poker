CREATE TABLE [players] (
  [uid] VARCHAR(32) NOT NULL ON CONFLICT FAIL CONSTRAINT [pk_user_id] UNIQUE ON CONFLICT FAIL,
  [login] VARCHAR(64) NOT NULL ON CONFLICT FAIL CONSTRAINT [unq_login] UNIQUE ON CONFLICT FAIL,
  [pass_hash] VARCHAR(32) NOT NULL ON CONFLICT FAIL,
  [name] VARCHAR(255) NOT NULL ON CONFLICT FAIL,
  [image_uid] VARCHAR(32),
  [is_automat] INTEGER NOT NULL ON CONFLICT FAIL,
  [ai_risk_level] INTEGER,
  [ai_skill] INTEGER,
  [total_money] REAL DEFAULT (0));


CREATE TABLE [player_statistic] (
  [player_uid] VARCHAR(32) NOT NULL ON CONFLICT FAIL CONSTRAINT [unq_player_id] UNIQUE ON CONFLICT FAIL CONSTRAINT [fk_players] REFERENCES [players]([uid]) ON DELETE CASCADE ON UPDATE CASCADE MATCH SIMPLE,
  [games] INTEGER DEFAULT (0),
  [winned] INTEGER DEFAULT (0),
  [failed] INTEGER DEFAULT (0),
  [interrupted] INTEGER DEFAULT (0),
  [scores] INTEGER DEFAULT (0));


