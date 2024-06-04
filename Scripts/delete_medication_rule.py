from tkinter import messagebox
from Scripts import connect_db
from Scripts import query

def delete_medication_rule(medication_rule_listbox,selected_medication_rule):

    meds = []
    for med in medication_rule_listbox.get(selected_medication_rule[0]):
        med_id = query.query("medication", "id", "name = ?", [str(med)])[0][0]
        meds.append(str(med_id))


    
    where = "medication_id1 = ? and medication_id2 = ?"
    if len(meds) > 2:
        for i in range(2,len(meds)):
            where1 += " and medication_id" + str(i+1) + " = ?"

    selected_medication_rule_id = query.query("medication_rules", "id", where, meds)
    
    if selected_medication_rule_id == []:
        messagebox.showwarning("Warning", "Problem deleting the rule. Please try again.")
        return
    
    # Connect to database    
    [c, conn] = connect_db.connect_db("lijnen.db")
    
    c.execute("DELETE FROM medication_rules WHERE id = ?", (selected_medication_rule_id[0][0],))
    medication_rule_listbox.delete(int(selected_medication_rule[0]))
    
    conn.commit()
    conn.close()
    