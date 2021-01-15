import sqlite3
from datetime import datetime
import model

# creating file path
dbfile = '/home/dani/Desktop/Python3/Flask/Homework3/todo.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
email = "dani"
#table_list = [a for a in cur.execute("SELECT password FROM users WHERE email = '{}' ORDER BY pk DESC".format(email))]
cur.execute("SELECT * FROM tasks;")
result = cur.fetchall()
# here is you table list
#print(table_list)

""" for i in result:
    print(str(i[0])+'. '+i[1]+' - '+str(i[2])) 
     """

# Be sure to close the connection
con.close()

email = "cvetaiii28@gmail.com"
idlist = 2
connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
cursor = connection.cursor()
cursor.execute("""SELECT * FROM lists;""")
todos = cursor.fetchall()

connection.commit()
cursor.close()
connection.close()

print("-"*49)
for i in todos:
    print(i)

print("-"*49)