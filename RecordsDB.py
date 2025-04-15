import sqlite3
from datetime import datetime


class RecordsDB:
    def __init__(self):
        self.conn = sqlite3.connect('game_records.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            completion_time REAL NOT NULL,
            level INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_level_time ON records (level, completion_time)')
        self.conn.commit()

    def add_record(self, player_name, completion_time, level):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO records (player_name, completion_time, level)
        VALUES (?, ?, ?)
        ''', (player_name, completion_time, level))
        self.conn.commit()

    def get_top_records(self, level=None, limit=10):
        cursor = self.conn.cursor()

        if level:
            cursor.execute('''
            SELECT player_name, completion_time, level, date 
            FROM records 
            WHERE level = ?
            ORDER BY completion_time ASC
            LIMIT ?
            ''', (level, limit))
        else:
            cursor.execute('''
            SELECT player_name, completion_time, level, date 
            FROM records 
            ORDER BY level ASC, completion_time ASC
            LIMIT ?
            ''', (limit,))

        records = cursor.fetchall()

        # Форматируем время
        formatted_records = []
        for name, time_sec, lvl, date in records:
            minutes = int(time_sec // 60)
            seconds = int(time_sec % 60)
            milliseconds = int((time_sec - int(time_sec)) * 1000)
            formatted_time = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
            formatted_records.append((name, formatted_time, lvl, date))

        return formatted_records

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
