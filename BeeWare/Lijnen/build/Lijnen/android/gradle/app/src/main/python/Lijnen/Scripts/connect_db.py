# script om verbinding te maken met de database

import sqlite3

def connect_db(database):
    # Maak verbinding met de opgegeven database
    try:
        conn = sqlite3.connect(database)
    except sqlite3.OperationalError as e:
        print(f"Fout bij het maken van de database: {e}")
    
    # Maak verbinding met de opgegeven database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    return c, conn