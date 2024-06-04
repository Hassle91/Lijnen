from Scripts import query
from Scripts import connect_db
from tkinter import messagebox

def delete_medication(medication_listbox, selected_medication):
    
    if selected_medication == ():
        return
    else:
        # Delete the medication from the database
        medication_name = medication_listbox.get(selected_medication)
        medication_id = query.query("medication", "id","name = ?" , (medication_name,))[0][0]
        medication_id_list = [medication_id]*8
    
        # Check if the medication is used in any rule
        [c, conn] = connect_db.connect_db("lijnen.db")
        c.execute("SELECT * FROM medication_rules \
                  WHERE medication_id1 = ? OR medication_id2 = ? OR medication_id3 = ? OR medication_id4 = ? OR medication_id5 = ? OR medication_id6 = ? OR medication_id7 = ? OR medication_id8 = ?" \
                  , medication_id_list)
        hits = c.fetchall()
        
        if hits != []:
            messagebox.showwarning("Warning", "This medication is used in a medication rule. Please remove the rule before deleting it.")
            return
        else:
            # messagebox.showwarning("Warning", "Deleted medication: " + medication_name)
            
            c.execute("DELETE FROM medication WHERE id = ?", (medication_id,))
        conn.commit()
        conn.close()    
        medication_listbox.delete(int(selected_medication[0]))
    



    