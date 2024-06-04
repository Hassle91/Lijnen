import tkinter as tk
from Scripts import load_medication

def update_medication_listbox(medication_listbox):

    # Clear the current listbox
    medication_listbox.delete(0, tk.END)

    # Get the updated medication list from the database
    _, medication_names = load_medication.load_medication()

    # Add the updated list to the listbox
    for medication in medication_names:
        medication_listbox.insert(tk.END, medication)