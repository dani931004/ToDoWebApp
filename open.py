import sqlite3
from datetime import datetime
import model
import flask_paginate
import inspect
import time


user = model.allUserTasks("dani")
print(user)
""" #Inspect flask-paginate
print(inspect.getsource(flask_paginate)) """




""" #Create 50 users
print(datetime.now())
start = datetime.now().timestamp()

name = "TousandUser"
password = "0410"

for n in range(1,1001):
    text = name + str(n)
    signup = model.signup(text, password)
print("Done!")

stop = datetime.now().timestamp()
print(stop - start)
print(datetime.now()) """


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