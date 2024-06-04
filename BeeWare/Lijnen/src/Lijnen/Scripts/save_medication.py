### Function to save medication
def save_medication(medication_name):
    # Get the value from the entry field
    medication = medication_name.get()

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