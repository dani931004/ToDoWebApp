import sqlite3
from datetime import datetime
import model




""" #Create 50 users
name = "user"
password = "0410"

for n in range(1,51):
    text = name + str(n)
    signup = model.signup(text, password)
 """


'''#Select all from lists table and print them
connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
cursor = connection.cursor()
cursor.execute("""SELECT * FROM lists;""")
todos = cursor.fetchall()

connection.commit()
cursor.close()
connection.close()

print(todos)

print("-"*80)
for i in todos:
    print(i)

print("-"*80)

'''