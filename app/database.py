import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Initialize Supabase client, but handle empty keys for local testing without .env
supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SCHEMA_SQL = """
-- Core Tables
CREATE TABLE IF NOT EXISTS leagues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    api_id INTEGER UNIQUE,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    api_match_id INTEGER UNIQUE,
    league_id INTEGER REFERENCES leagues(id),
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    kickoff_time TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS goal_events (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id),
    scoring_team VARCHAR(10),
    minute INTEGER,
    half INTEGER
);

CREATE TABLE IF NOT EXISTS match_stats (
    id SERIAL PRIMARY KEY,
    match_id INTEGER UNIQUE REFERENCES matches(id),
    home_corners INTEGER,
    away_corners INTEGER,
    home_yellow_cards_ht INTEGER,
    away_yellow_cards_ht INTEGER,
    penalty_awarded BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    current_balance DECIMAL(12,2),
    kelly_multiplier DECIMAL(3,2) DEFAULT 0.25,
    signals_active BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS bet_ledger (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profiles(id),
    market VARCHAR(100),
    odds DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'pending',
    result VARCHAR(10)
);
"""

def init_db():
    """
    Function to document the schema.
    In a real app, you would run this via Supabase dashboard or migrations.
    For this setup, the schema is documented above.
    """
    print("Database schema defined. Run SCHEMA_SQL in your Supabase SQL editor.")
    pass
