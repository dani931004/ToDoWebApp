import sqlite3
from datetime import datetime

# creating file path
dbfile = '/home/dani/Desktop/Python3/Flask/Homework3/todo.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
email = "dani"
#table_list = [a for a in cur.execute("SELECT password FROM users WHERE email = '{}' ORDER BY pk DESC".format(email))]
cur.execute("SELECT name,date FROM lists ORDER BY pk DESC")
result = cur.fetchall()
# here is you table list
#print(table_list)
for i in result:
    text = i
    print('('+text[0]+','+str(text[1])+')')
    

# Be sure to close the connection
con.close()


connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
cursor = connection.cursor()
cursor.execute("""SELECT * FROM lists""")
todos = cursor.fetchall() 
for todo in todos:
    
    print(todo)