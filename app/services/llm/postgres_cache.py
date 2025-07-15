from datetime import datetime
from psycopg2.extras import Json
from langchain_core.caches import BaseCache


class PostgresCache(BaseCache):
    def __init__(self, conn):
        self.conn = conn
        self._ensure_table()

    def _ensure_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS llm_cache (
                    key TEXT PRIMARY KEY,
                    value JSONB NOT NULL,
                    llm_string TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            self.conn.commit()

    def _get_cache_key(self, prompt, llm_string):
        return f"{prompt}|||{llm_string}"

    def lookup(self, prompt, llm_string=None):
        key = self._get_cache_key(prompt, llm_string)
        # print("Buscando em cache")
        with self.conn.cursor() as cur:
            cur.execute("SELECT value FROM llm_cache WHERE key = %s;", (key,))
            result = cur.fetchone()
            return result[0] if result else None

    def update(self, prompt, llm_string, return_val):
        key = self._get_cache_key(prompt, llm_string)
        generations = [{"text": g.text if hasattr(g, "text") else str(g)} for g in return_val]
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO llm_cache (key, value, llm_string, created_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (key) DO UPDATE
                SET value = EXCLUDED.value,
                    llm_string = EXCLUDED.llm_string,
                    created_at = EXCLUDED.created_at;
            """, (key, Json(generations), llm_string, datetime.utcnow()))
            self.conn.commit()

    def clear(self):
        """Implementação obrigatória da interface BaseCache."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM llm_cache;")
            self.conn.commit()
