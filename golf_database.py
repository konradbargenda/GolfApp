import sqlite3
import tkinter as tk
from tkinter import messagebox

import sqlite3

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('golf_app.db')
            self.c = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise

    def create_tables(self):
        try:
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT,
                    points TEXT,
                    notes TEXT,
                    date TEXT,
                    hours_of_sleep TEXT,
                    how_you_feel TEXT,
                    meals TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.c.execute('''
                CREATE TABLE IF NOT EXISTS golf_rounds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    par INTEGER,
                    score INTEGER,
                    fairways_hit INTEGER,
                    fairways_attempted INTEGER,
                    greens_hit INTEGER,
                    greens_attempted INTEGER,
                    putts INTEGER,
                    up_downs INTEGER,
                    up_down_attempts INTEGER,
                    notes TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def save_journal_entry(self, entry):
        try:
            time = entry.get("Time", "")
            points = entry.get("Points", "")
            notes = entry.get("Notes", "")
            date = entry.get("Date", "")
            hours_of_sleep = entry.get("Hours of Sleep", "")
            how_you_feel = entry.get("How You Feel", "")
            meals = entry.get("Meals", "")

            self.c.execute(
                '''
                INSERT INTO journal_entries (time, points, notes, date, hours_of_sleep, how_you_feel, meals)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (str(time), str(points), str(notes), str(date), str(hours_of_sleep), str(how_you_feel), str(meals))
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving journal entry: {e}")
            raise
    def get_all_journal_entries(self):
        try:
            self.c.execute("SELECT * FROM journal_entries ORDER BY timestamp DESC")
            rows = self.c.fetchall()
            journal_entries = []
            for row in rows:
                journal_entries.append({
                    "ID": row[0],
                    "Time": row[1],
                    "Points": row[2],
                    "Notes": row[3],
                    "Date": row[4],
                    "Hours of Sleep": row[5],
                    "How You Feel": row[6],
                    "Meals": row[7],
                    "Timestamp": row[8]
                })
            return journal_entries
        except sqlite3.Error as e:
            print(f"Error retrieving journal entries: {e}")
            raise


    def save_round(self, par, score, fairways_hit, fairways_attempted, greens_hit, greens_attempted,
                   putts, up_downs, up_down_attempts, notes):
        try:
            self.c.execute(
                '''
                INSERT INTO golf_rounds (par, score, fairways_hit, fairways_attempted, greens_hit, greens_attempted,
                                         putts, up_downs, up_down_attempts, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (par, score, fairways_hit, fairways_attempted, greens_hit, greens_attempted,
                 putts, up_downs, up_down_attempts, notes)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving round: {e}")
            raise

    def get_all_rounds(self):
        try:
            self.c.execute("SELECT * FROM golf_rounds ORDER BY timestamp DESC")
            rows = self.c.fetchall()
            rounds = []
            for row in rows:
                rounds.append({
                    "ID": row[0],
                    "Par": row[1],
                    "Score": row[2],
                    "Fairways Hit": row[3],
                    "Fairways Attempted": row[4],
                    "Greens Hit": row[5],
                    "Greens Attempted": row[6],
                    "Putts": row[7],
                    "Up-and-Downs": row[8],
                    "Up-and-Down Attempts": row[9],
                    "Notes": row[10],
                    "Timestamp": row[11]
                })
            return rounds
        except sqlite3.Error as e:
            print(f"Error retrieving rounds: {e}")
            raise

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")
            raise
