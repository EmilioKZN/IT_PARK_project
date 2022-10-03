import sqlite3
from botik import answers_and_right_str

def write_base():
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    if answers_and_right_str():
        cur.execute("""INSERT INTO 'Dinamicbd'(country, capital, url) VALUES (?, ?, ?);""", answers_and_right_str()[0][1:])
        base.commit()

#write_base()

def get_str():
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    return cur.execute("SELECT * FROM 'Dinamicbd'").fetchone()

# print(get_str())

def clear_base():
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    cur.execute("""DELETE FROM 'Dinamicbd'""")
    base.commit()
    cur.close()

#clear_base()

