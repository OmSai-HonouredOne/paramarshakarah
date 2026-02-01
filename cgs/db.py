import psycopg2, psycopg2.extras
from psycopg2 import pool
from flask import current_app, g

db_pool = None

def init_db_pool(app):
    global db_pool
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=app.config['DATABASE_URL'],
        sslmode='require',
        cursor_factory=psycopg2.extras.DictCursor
    )

def get_db():
    if 'db' not in g:
        g.db = db_pool.getconn()
    return g.db

def release_db():
    db = g.pop('db', None)
    if db is not None:
        db_pool.putconn(db)

def query_one(sql, params=None):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()

def query_all(sql, params=None):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def execute(sql, params=None):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params)
    db.commit()

def close_db(e=None):
    release_db()

def init_app(app):
    init_db_pool(app)           # initialize the pool once
    app.teardown_appcontext(close_db)