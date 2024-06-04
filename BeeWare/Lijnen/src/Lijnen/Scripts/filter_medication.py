# functie om de medicatie uit de database te laden en filteren
from Scripts import load_medication
import tkinter as tk

def filter_medication(medication_listbox,search_term):
        
        
        [medication_ids , medication_names] = load_medication.load_medication()
        filtered_medication = [med for med in medication_names if search_term.lower() in med.lower()]
        medication_listbox.delete(0, tk.END)
        for med in filtered_medication:
            medication_listbox.insert(tk.END, med)

        return medication_listbox