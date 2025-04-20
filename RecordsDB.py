import sqlite3
import os
from datetime import datetime


class RecordsDB:
    def __init__(self):
        self.db_file = 'game_records.db'
        try:
            # Проверяем доступность файла БД
            if not os.path.exists(self.db_file):
                open(self.db_file, 'w').close()

            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute("PRAGMA journal_mode=WAL")  # Режим журналирования
            self.create_table()
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            raise

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                completion_time INTEGER NOT NULL,
                level INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_level_time 
            ON records (level, completion_time)''')
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")
            raise

    def add_record(self, player_name, completion_time, level):
        try:
            # Проверка входных данных
            if not player_name or not isinstance(completion_time, (int, float)) or not isinstance(level, int):
                raise ValueError("Некорректные данные для записи")

            time_ms = int(completion_time * 1000)
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO records (player_name, completion_time, level)
            VALUES (?, ?, ?)''', (player_name[:50], time_ms, level))  # Ограничиваем длину имени

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка записи рекорда: {e}")
            self.conn.rollback()
            return False

    def get_top_records(self, level=None, limit=10):
        try:
            cursor = self.conn.cursor()

            if level:
                cursor.execute('''
                SELECT player_name, completion_time, level, datetime(date, 'localtime') 
                FROM records 
                WHERE level = ?
                ORDER BY completion_time ASC
                LIMIT ?''', (level, limit))
            else:
                cursor.execute('''
                SELECT player_name, completion_time, level, datetime(date, 'localtime') 
                FROM records 
                ORDER BY level ASC, completion_time ASC
                LIMIT ?''', (limit,))

            records = cursor.fetchall()
            formatted_records = []

            for name, time_ms, lvl, date in records:
                try:
                    total_seconds = time_ms / 1000
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    milliseconds = int(time_ms % 1000)
                    formatted_time = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
                    formatted_records.append((name, formatted_time, lvl, date))
                except Exception as e:
                    print(f"Ошибка форматирования записи: {e}")
                    continue

            return formatted_records
        except Exception as e:
            print(f"Ошибка получения рекордов: {e}")
            return []

    def close(self):
        try:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Ошибка закрытия БД: {e}")

    def __del__(self):
        self.close()

    def clear_all_records(self):
        """Очищает все записи из базы данных"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM records')
        self.conn.commit()