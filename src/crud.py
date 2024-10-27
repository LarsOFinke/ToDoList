import os, sys, sqlite3


def get_db_path():
    # Get the directory of the executable
    if hasattr(sys, '_MEIPASS'):
        # If running as a PyInstaller executable
        return os.path.join(sys._MEIPASS, 'Database.db')
    else:
        # If running as a script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Database.db')



CONNECTIONSTRING = get_db_path()




def create_database():
    con = sqlite3.connect(CONNECTIONSTRING)
    cursor = con.cursor()
    with con:
        sql: str =  "CREATE TABLE tblLists(" \
                    "ListID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                    "ListName TEXT NOT NULL UNIQUE)"
        cursor.execute(sql)
        
        sql: str =  "CREATE TABLE tblEntries(" \
                    "EntryID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                    "EntryContent TEXT NOT NULL, " \
                    "ListIDRef INTEGER)"
        cursor.execute(sql)
        

if not os.path.exists(CONNECTIONSTRING):
    create_database()
    


# CREATE SQLITE3 CONSTANTS for CONNECTION
CON = sqlite3.connect(CONNECTIONSTRING)
CURSOR = CON.cursor()



def create_list(name: str) -> None:
    with CON:
        sql: str = "INSERT INTO tblLists(ListName) VALUES (?)"
        CURSOR.execute(sql, (name,))


def get_lists() -> dict:
    lists: dict = {}    # {"Name" : ListID}
    with CON:
        sql: str = "SELECT * FROM tblLists"
        CURSOR.execute(sql)
        
        for lst in CURSOR:
            lists.update({lst[1]: lst[0]})
            
        return lists
        

def update_listname(name: str, listID: int):
    with CON:
        sql: str = "UPDATE tblLists SET ListName = ? WHERE ListID = ?"
        CURSOR.execute(sql, (name, listID))


def delete_list(listID: int) -> None:
    with CON:
        sql: str = "DELETE FROM tblLists WHERE ListID = ?"
        CURSOR.execute(sql, (listID,))
        
        try:
            sql: str = "DELETE FROM tblEntries WHERE ListID = ?"
            CURSOR.execute(sql, (listID,))
        except:
            return




def add_entry(content: str, listID: int) -> None:
    with CON:
        sql: str = "INSERT INTO tblEntries(EntryContent, ListIDRef) VALUES (?,?)"
        CURSOR.execute(sql, (content, listID))


def get_entries(listID: int) -> dict:
    entries: dict = {}  # {"Content" : ID}
    with CON:
        sql: str = "SELECT EntryID, EntryContent FROM tblEntries WHERE ListIDRef = ?"
        CURSOR.execute(sql, (listID,))
        
        for entry in CURSOR:
            entries.update({entry[1] : entry[0]})
            
        return entries


def edit_entry(content: str, entryID: int) -> None:
    with CON:
        sql: str = "UPDATE tblEntries SET EntryContent = ? WHERE EntryID = ?"
        CURSOR.execute(sql, (content, entryID))


def delete_entry(entryID: int) -> None:
    with CON:
        sql: str = "DELETE FROM tblEntries WHERE EntryID = ?"
        CURSOR.execute(sql, (entryID,))
