import os

import psycopg2
import psycopg2.extras
import psycopg2.pool

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "ec_practice")

_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
)


def get_db():
    """FastAPIのDependsで使うカーソル取得関数。
    リクエスト単位でコネクションをプールから借り、正常終了時はcommit、例外時はrollbackする。
    """
    conn = _pool.getconn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)
