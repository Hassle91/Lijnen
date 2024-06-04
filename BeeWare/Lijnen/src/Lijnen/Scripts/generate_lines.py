from tkinter import messagebox
from Scripts import connect_db
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from Scripts import optimalisatie
from Scripts import query

def generate_lines(selected_medication, max_per_lijn):
    
    # Connect to the database
    [c, conn] = connect_db.connect_db("lijnen.db")

    # Check if the medication is used in any rule
    ids = []

    for name in selected_medication.get(0, "end"):
        name = query.query("medication", "id", "name = '" + name + "'")[0][0]
        ids.append(name)

    # Maak de tabel 'medication_rules' als deze nog niet bestaat
    c.execute("CREATE TABLE IF NOT EXISTS medication_rules (id INTEGER PRIMARY KEY, medication_id1 INTEGER, medication_id2 INTEGER, medication_id3 INTEGER, medication_id4 INTEGER, medication_id5 INTEGER, medication_id6 INTEGER, medication_id7 INTEGER, medication_id8 INTEGER)")

    all_relevant_rules = []
    for id in ids:
        c.execute("SELECT * FROM medication_rules \
                WHERE medication_id1 = ? OR medication_id2 = ? \
                OR medication_id3 = ? OR medication_id4 = ? \
                OR medication_id5 = ? OR medication_id6 = ? \
                OR medication_id7 = ? OR medication_id8 = ?", [id]*8)
        rules = c.fetchall()
        if rules != []:
            for rule in rules:
                if rule not in all_relevant_rules:
                    all_relevant_rules.append(rule)
    
    rules = []
    for rule in all_relevant_rules:
        new_rule = []
        for medication_id in rule[1:]:
            if medication_id != None and medication_id in ids:
                new_rule.append(medication_id)
        if len(new_rule) > 1:
            rules.append(new_rule)

    for rule in rules:
        for id in rule:
            if id not in ids:
                ids.append(id)

    groups = optimalisatie.optimalisatie(ids, rules, max_per_lijn)
    # print(groups)

    return groups,ids,rules    

    # get the names of the medication and visualize the groups



    
    
        



    
        
    

    
    