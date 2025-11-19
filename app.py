from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import sqlite3, time, random, os
from pydantic import BaseModel

DB = 'ucpusa_prod.db'
app = FastAPI()

# --- Утилиты ---
def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    return conn

def register_user_if_needed(user_id=1, username='WebUser'):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO users (user_id, username, comm_coins, energy, last_daily) VALUES (?, ?, 100, 100, '')''', (user_id, username))
        cursor.execute('INSERT OR IGNORE INTO economy (user_id) VALUES (?)', (user_id,))
        cursor.execute('INSERT OR IGNORE INTO revolution (user_id) VALUES (?)', (user_id,))
        cursor.execute('INSERT OR IGNORE INTO voting (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

# Ensure DB schema exists (port init_db skeleton)
def ensure_schema():
    if not os.path.exists(DB):
        conn = get_conn()
        cur = conn.cursor()
        # simplified schema: users, economy, revolution, inventory, voting
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, comm_coins INTEGER DEFAULT 100, last_work INTEGER DEFAULT 0, last_daily TEXT, energy INTEGER DEFAULT 100, party_rank TEXT DEFAULT 'Новичок', reputation INTEGER DEFAULT 0, casino_wins INTEGER DEFAULT 0, casino_losses INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, factories INTEGER DEFAULT 0, farms INTEGER DEFAULT 0, shops INTEGER DEFAULT 0, companies INTEGER DEFAULT 0, last_collect INTEGER DEFAULT 0, factory_limit INTEGER DEFAULT 5, farm_limit INTEGER DEFAULT 5, shop_limit INTEGER DEFAULT 5, company_limit INTEGER DEFAULT 5);
        CREATE TABLE I
