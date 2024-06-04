import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from Scripts import load_medication
from Scripts import load_medication_rules
from Scripts import connect_db
from Scripts import update_medication_listbox
from Scripts import filter_medication
from Scripts import delete_medication
from Scripts import generate_lines
from Scripts import query
from Scripts import delete_medication_rule

[medication_ids, medication_names] = load_medication.load_medication()

# Hoofd Tkinter venster setup
main_window = tk.Tk()
main_window.title("Lijnen indeling tool")
main_window.configure(bg='green')
pos_main = "+"+str(main_window.winfo_screenwidth()//4)+"+"+str(main_window.winfo_screenheight()//4)
main_window.geometry(pos_main)

# maak een knop om het maximale aantal medicamenten per lijn in te stellen
# max_per_lijn = tk.StringVar(main_window)
# max_per_lijn.set("5")  # standaardwaarde
# options = [str(i) for i in range(2, 9)]  # lijst van opties van 2 tot 8
# max_menu = tk.OptionMenu(main_window, max_per_lijn, *options)
# max_menu.grid(row=1, column=2)
# max_per_lijn_value = 5
# def update_max_per_lijn(*args):
#     global max_per_lijn_value
#     max_per_lijn_value = int(max_per_lijn.get())

# max_per_lijn.trace("w", update_max_per_lijn)

# label max per lijn
# tk.Label(main_window, text="Max meds per lijn").grid(row=0, column=2)

# Medicatie lijst setup
tk.Label(main_window, text="Medicatielijst").grid(row=0, column=0)
medication_listbox = tk.Listbox(main_window)
update_medication_listbox.update_medication_listbox(medication_listbox)
medication_listbox.grid(row=2, column=0)

# filterveld
filter_entry = tk.Entry(main_window)
filter_entry.grid(row=1, column=0)

# filterknop
filter_button = tk.Button(main_window, text="Filter", command=lambda: filter_medication.filter_medication(medication_listbox,filter_entry.get()))
filter_button.grid(row=1, column=1, sticky="w")

# Geselecteerde medicatie label
tk.Label(main_window, text="Geselecteerde Medicatie").grid(row=0, column=3)

# Geselecteerde medicaties listbox
selected_medication = tk.Listbox(main_window)
# selected_medication.insert(tk.END, "a","b","c","d","e","f","g","asperine","paracetamol")
selected_medication.grid(row=2, column=3, sticky="w")

# Button to add selected medication to the listbox
def add_medication_to_selection():
    if medication_listbox.curselection() == ():
        return
    if medication_listbox.get(medication_listbox.curselection()) not in selected_medication.get(0, tk.END):
        selected_medication.insert(tk.END, medication_listbox.get(medication_listbox.curselection()))

add_button = tk.Button(main_window, text=">", command=add_medication_to_selection)
add_button.grid(row=2, column=1)

# Button to add all medication to the listbox
def add_all_medication_to_selection():
    for medication in medication_listbox.get(0, tk.END):
        if medication not in selected_medication.get(0, tk.END):
            selected_medication.insert(tk.END, medication)

add_all_button = tk.Button(main_window, text=">>", command=add_all_medication_to_selection)
add_all_button.grid(row=2, column=2)

# Knop om geselecteerd item te verwijderen
def remove_selected_item():
    selected = selected_medication.curselection()
    if selected:  # If there is a selected item
        selected_medication.delete(selected)  # Remove the selected item

remove_button = tk.Button(main_window, text="<", command=remove_selected_item)
remove_button.grid(row=2, column=2, sticky="s")

# knop om alle medicatie te verwijderen
def remove_all_items():
    selected_medication.delete(0, tk.END)

remove_all_button = tk.Button(main_window, text="<<", command=remove_all_items)
remove_all_button.grid(row=2, column=1, sticky="s")

# display output op optimalisatie
tk.Label(main_window, text="Lijnen").grid(row=0, column=4)
result_listbox = tk.Listbox(main_window)
result_listbox.grid(row=2, column=4)

def lijnen_to_listbox(selected_medication,max_per_lijn_value):
    [groups,ids,rules] = generate_lines.generate_lines(selected_medication,100)
    
    # Clear the ListBox
    if result_listbox != None:
        result_listbox.delete(0, tk.END)

    # query the name by id
    med_groups = []
    for group in groups:
        med_groups.append(group)
        for med in group:
            result = query.query("medication", "name", "id = " + str(med))
            med_groups[-1][med_groups[-1].index(med)] = result[0][0]

    # Calculate the maximum length of the items
    for group in med_groups:
        total_chars = 0
        for chars in group:
            total_chars += len(chars)
            if (total_chars+10) > result_listbox.cget("width"):                
                result_listbox.config(width=(total_chars+10))    

    # Add the result to the ListBox
    if isinstance(groups, list):  # if the result is a list
        for group in med_groups:
            result_listbox.insert(tk.END, group)
    else:  # if the result is a single value
        result_listbox.insert(tk.END, groups)

# Update the listbox when the window is focused
main_window.bind('<FocusIn>', lambda event: update_medication_listbox.update_medication_listbox(medication_listbox))

# Functie om nieuwe medicatie in te voeren
def add_medication():
    global add_medication_window
    # Maak een nieuw venster
    add_medication_window = tk.Toplevel()
    pos_med_add = "+"+str(main_window.winfo_screenwidth()//8*6)+"+"+str(main_window.winfo_screenheight()//4)
    add_medication_window.geometry(pos_med_add)
    add_medication_window.configure(bg='green')

    # Maak een invoerveld voor de medicatie
    new_medication_entry = tk.Entry(add_medication_window)
    new_medication_entry.grid(row=0, column=0)

    # Create a button to save the medication
    save_medication_button = tk.Button(add_medication_window, text="Opslaan", command=lambda: save_medication(new_medication_entry))
    save_medication_button.grid(row=1, column=0)

### Function to save medication
def save_medication(medication_name):
    # Get the value from the entry field
    medication = medication_name.get()

    if medication == "":
        return
    # Connect to the database
    [c, conn] = connect_db.connect_db("lijnen.db")

    # Check if the medication name already exists
    c.execute("SELECT name FROM medication WHERE name = ?", (medication,) )
    if c.fetchone() is not None:
        # If the medication name already exists, show a warning message and return
        messagebox.showwarning("Warning", "Dit medicament staat reeds in de lijst")
        return
    
    # Insert the new medication into the 'medication' table
    c.execute("INSERT INTO medication (name) VALUES (?)", (medication,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    tk.Toplevel.destroy(add_medication_window)

# definitie van de medication_window functie die een overzicht geeft van de medicatie in de database
def medication_window():
    medication_window = tk.Toplevel()
    medication_window.title("Medicatielijst")
    medication_window.configure(bg='green')
    pos_med = "+"+str(main_window.winfo_screenwidth()//8*5)+"+"+str(main_window.winfo_screenheight()//4)
    medication_window.geometry(pos_med)

    # knop om de add_medication_window te openen
    add_medication_window_button = tk.Button(medication_window, text="Voeg medicatie toe", command=add_medication)
    add_medication_window_button.grid(row=1, column=1)

    # Laad de medicatie uit de database
    _, medication_names = load_medication.load_medication()

    # Medicatie lijst setup
    medication_listbox_2 = tk.Listbox(medication_window)
    medication_listbox_2.grid(row=1, column=0)
    for medication in medication_names:
        medication_listbox_2.insert(tk.END, medication)

    #filterveld
    filter_entry = tk.Entry(medication_window)
    filter_entry.grid(row=0, column=0)
 
    #filterknop
    filter_button = tk.Button(medication_window, text="Filter", command=lambda: filter_medication.filter_medication(medication_listbox_2,filter_entry.get()))
    filter_button.grid(row=0, column=1)

    # Button to delete the selected medication
    delete_button = tk.Button(medication_window, text="Verwijder", command=lambda: delete_medication.delete_medication(medication_listbox_2, medication_listbox_2.curselection()))
    delete_button.grid(row=1, column=1, sticky="s")

    # Update the listbox when the window is focused
    medication_window.bind('<FocusIn>', lambda event: update_medication_listbox.update_medication_listbox(medication_listbox_2))

def medication_rules_window():

    # Maak een nieuw venster
    medication_rules_window = tk.Toplevel(main_window)
    medication_rules_window.title("Medicatieregels")
    medication_rules_window.configure(bg='green')
    pos_rules = "+"+str(main_window.winfo_screenwidth()//8*5)+"+"+str(main_window.winfo_screenheight()//4)
    medication_rules_window.geometry(pos_rules)

    # Label voor de medicatieregels
    tk.Label(medication_rules_window, text="Medicatieregels").grid(row=0, column=0)

    # Maak een nieuwe knop die de add_medication_rule functie aanroept
    new_medication_rule_button = tk.Button(medication_rules_window, text="Nieuw", command=add_medication_rule)
    new_medication_rule_button.grid(row=1, column=1, sticky="n")

    # Maak een nieuwe knop die de delete_medication_rule functie aanroept
    delete_medication_rule_button = tk.Button(medication_rules_window, text="Verwijder", command=lambda: delete_medication_rule.delete_medication_rule(medication_rules_listbox, medication_rules_listbox.curselection()))
    delete_medication_rule_button.grid(row=1, column=1)

    # Maak een listbox voor de medicatieregels
    medication_rules_listbox = tk.Listbox(medication_rules_window)
    medication_rules_listbox.grid(row=0, column=0)    
    update_rules_listbox(medication_rules_listbox)
    # Calculate the maximum length of the items
  
    medication_rules_window.bind('<FocusIn>', lambda event: update_rules_listbox(medication_rules_listbox))

def update_rules_listbox(medication_rules_listbox):
    medication_rules = []
    medication_rules_listbox.delete(0, tk.END)
    medication_rules= load_medication_rules.load_medication_rules()
    for rule in medication_rules:
        medication_rules_listbox.insert(tk.END, rule)
    medication_rules_listbox.grid(row=1, column=0)

    for rule in medication_rules:
        total_chars = 0
        for chars in rule:
            total_chars += len(chars)
            if (total_chars+10) > medication_rules_listbox.cget("width"):                
                medication_rules_listbox.config(width=(total_chars+10))

def add_medication_rule():
    global add_medication_rule_window
    # Maak een nieuw venster
    add_medication_rule_window = tk.Toplevel()
    add_medication_rule_window.title("Nieuwe medicatieregel")
    add_medication_rule_window.configure(bg='green')
    pos_rules_add = "+"+str(main_window.winfo_screenwidth()//8*6)+"+"+str(main_window.winfo_screenheight()//4)
    add_medication_rule_window.geometry(pos_rules_add)

    [medication_ids, medication_names] = load_medication.load_medication()

    tk.Label(add_medication_rule_window, text="Selecteer medicatie die niet samen over 1 lijn mag").grid(row=0, column=0)

    # Create a combobox for each medication
    combobox1 = ttk.Combobox(add_medication_rule_window, values=medication_names)
    combobox1.grid(row=1, column=0)

    combobox2 = ttk.Combobox(add_medication_rule_window, values=medication_names)
    combobox2.grid(row=2, column=0)

    # Create a button to save the medication rule
    save_medication_rule_button = tk.Button(add_medication_rule_window, text="Opslaan", command=lambda: save_medication_rule(medication_ids,[combobox1.current(), combobox2.current()]))
    save_medication_rule_button.grid(row=1, column=1)

def save_medication_rule(medication_ids,selected_values):
    
    if -1 in selected_values:
        messagebox.showwarning("Warning", "In beide velden moet een medicijn geselecteerd zijn")
        return
    # Connect to the database
    [c, conn] = connect_db.connect_db("lijnen.db")
    
    selected_ids = [medication_ids[i] for i in selected_values]

    while len(selected_ids) < 8:
        selected_ids.append(None)

    if selected_ids[0] == selected_ids[1]:
        messagebox.showwarning("Warning", "De medicatie mag niet hetzelfde zijn")
        return
    elif selected_ids[0] == None or selected_ids[1] == None:
        messagebox.showwarning("Warning", "In beide velden moet een medicijn geselecteerd zijn")
        return
    # Insert the selected values into the 'medication_rules' table
    c.execute("INSERT INTO medication_rules (medication_id1, medication_id2, medication_id3, medication_id4, medication_id5, medication_id6, medication_id7, medication_id8) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", selected_ids)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    tk.Toplevel.destroy(add_medication_rule_window)

# knop die de medication_window scherm opent
medication_window_button = tk.Button(main_window, text="Toon Medicatielijst", command=medication_window)
medication_window_button.grid(row=7, column=0, sticky="w")

# knop die medicatieregels_scherm opent
medication_rules_window_button = tk.Button(main_window, text="Toon Medicatieregels", command=medication_rules_window)
medication_rules_window_button.grid(row=8, column=0, sticky="w")

# knop die lijnen genereerd
generate_lines_button = tk.Button(main_window, text="Genereer lijnen", command=lambda: lijnen_to_listbox(selected_medication, 100))
generate_lines_button.grid(row=4, column=3, sticky="w")

main_window.mainloop()