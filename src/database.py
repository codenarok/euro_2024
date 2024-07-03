# src/database.py

import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('data/euro_2024.db')
    return conn

def create_tables(conn):
    """Create tables in the SQLite database."""
    create_groups_table = """
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL,
        team_name TEXT NOT NULL,
        points INTEGER DEFAULT 0,
        goal_difference INTEGER DEFAULT 0,
        goals_scored INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        UNIQUE(group_name, team_name)
    );
    """
    create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL,
        team1 TEXT NOT NULL,
        team2 TEXT NOT NULL,
        team1_goals INTEGER,
        team2_goals INTEGER
    );
    """
    conn.execute(create_groups_table)
    conn.execute(create_matches_table)
    conn.commit()

def initialize_database():
    """Initialize the database by creating the necessary tables."""
    conn = create_connection()
    create_tables(conn)
    conn.close()

if __name__ == '__main__':
    initialize_database()
