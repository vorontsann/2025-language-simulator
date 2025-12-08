import sqlite3
from pathlib import Path


class SQLiteUserManager:
    def __init__(self, db_path: str = "data/users.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    total_answers INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    # ===== CRUD операции =====

    def create_user(self, username: str) -> int:
        """Создать нового пользователя, вернуть его id"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username) VALUES (?)",
                (username,)
            )
            conn.commit()
            return cursor.lastrowid

    def get_user_by_name(self, username: str):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, total_answers, correct_answers FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone()

    def update_stats(self, user_id: int, is_correct: bool):
        """Обновить статистику пользователя"""
        with self._connect() as conn:
            cursor = conn.cursor()
            if is_correct:
                cursor.execute("""
                    UPDATE users
                    SET total_answers = total_answers + 1,
                        correct_answers = correct_answers + 1
                    WHERE id = ?
                """, (user_id,))
            else:
                cursor.execute("""
                    UPDATE users
                    SET total_answers = total_answers + 1
                    WHERE id = ?
                """, (user_id,))

            conn.commit()

    def get_user_stats(self, user_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT total_answers, correct_answers
                FROM users
                WHERE id = ?
            """, (user_id,))
            return cursor.fetchone()
