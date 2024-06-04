import tkinter as tk
from Scripts import connect_db

def load_medication_rules():

# connectie maken met de database
    [c, conn] = connect_db.connect_db("lijnen.db")

    # Controleer of de tabel bestaat
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medication_rules'")
    if c.fetchone() is None:
        c.execute('''
            CREATE TABLE medication_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medication_id1 INTEGER NOT NULL,
                medication_id2 INTEGER NOT NULL,
                medication_id3 INTEGER,
                medication_id4 INTEGER,
                medication_id5 INTEGER,
                medication_id6 INTEGER,
                medication_id7 INTEGER,
                medication_id8 INTEGER,
                UNIQUE (medication_id1, medication_id2, medication_id3, medication_id4, medication_id5, medication_id6, medication_id7, medication_id8)
            )
        ''')
        conn.commit()

    # Haal de medicatieregels op uit de database
    c.execute('''
                SELECT m1.name, m2.name, m3.name, m4.name, m5.name, m6.name, m7.name, m8.name
                from medication_rules r
                left join medication m1 on r.medication_id1 = m1.id
                left join medication m2 on r.medication_id2 = m2.id
                left join medication m3 on r.medication_id3 = m3.id
                left join medication m4 on r.medication_id4 = m4.id
                left join medication m5 on r.medication_id5 = m5.id
                left join medication m6 on r.medication_id6 = m6.id
                left join medication m7 on r.medication_id7 = m7.id
                left join medication m8 on r.medication_id8 = m8.id
    ''')
    medication_rules = c.fetchall()

    rules = []
    
    for rule in medication_rules:
        rule_list = [med for med in rule if med is not None]
        rules.append(rule_list)

    return rules