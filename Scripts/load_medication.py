import sqlite3
import os
from Scripts import connect_db
# Functie om medicatie uit de database te laden
def load_medication():

    [c, conn] = connect_db.connect_db("lijnen.db")
    
    # Maak de tabel 'medication' als deze nog niet bestaat
    c.execute("CREATE TABLE IF NOT EXISTS medication (id INTEGER PRIMARY KEY, name TEXT)")

    # Haal de medicaties uit de database
    c.execute("SELECT id, name FROM medication ORDER BY name ASC")
    medication_db = c.fetchall()
    
    # Voeg de medicatie toe aan de 'medication' lijst
    medication_ids = [medication[0] for medication in medication_db]
    medication_names = [medication[1] for medication in medication_db]

    # Sluit de verbinding met de database
    conn.close()

    return medication_ids, medication_names