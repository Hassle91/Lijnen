from Scripts import connect_db

def query(TABLE, COLUMNS, WHERE, PARAMS = []):
    [c, conn] = connect_db.connect_db("lijnen.db")
    if WHERE == "":
        c.execute("SELECT " + COLUMNS + " FROM " + TABLE)
    else:
        query = f"SELECT {COLUMNS} FROM {TABLE} WHERE {WHERE}"
        # print(query, PARAMS)
        c.execute(query, PARAMS)
    result = c.fetchall()
    
    return result