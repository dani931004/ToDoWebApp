import sqlite3
from datetime import datetime

#Check if password is right
def check_pw(email):
    
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE email like '{}' ORDER BY pk DESC;""".format(email))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    
    return password

def check_pw_adm(email):
    
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM admin WHERE email = '{}' ORDER BY pk DESC;""".format(email))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    
    return password

#Select usernames signed up in the last 24hours
def last24h():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT email FROM users WHERE "datetime" >=DATETIME("now","-1 day");""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo


#Select all Lists created in the last 24hours
def last24hLists():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT name FROM lists WHERE "date" >=DATETIME("now","-1 day");""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo


#Total Lists created
def totalLists():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM lists ;""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Sign up the user
def signup(email, password):
    now = datetime.now()
    today = now.strftime("%Y/%m/%d %H:%M:%S")
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE email = '{}';""".format(email))
    exist = cursor.fetchone() 
    
    if exist is None:
        cursor.execute("""INSERT INTO users(email,password,datetime)VALUES('{}', '{}','{}');""".format(email,password,today))
        
        connection.commit()
        cursor.close()
        connection.close()
    
    else:
        return ('User already exists!!!')
    
    return 'You have signed up successfully!'

#Returns all the users
def check_users():
    
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT email FROM users;""")
    db_users = cursor.fetchall()
    users = []
    
    
    for i in range((len(db_users))):
        person = db_users[i][0]
        users.append(person)
    
    
    
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return users

#Show all users on DB
def allUsers():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users;""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Select list by ID
def selList(username):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM lists WHERE email = '{}';""".format(username))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return todo

#Select task by ID of list
def selTask(idlist,username):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM tasks WHERE (idlistt = '{}' and email = '{}');""".format(idlist,username))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return todo

#Create list on DB
def createList(name,email):
    now = datetime.now()
    today = now.strftime("%Y/%m/%d %H:%M:%S")
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT name FROM lists WHERE (name = '{}' and email = '{}');""".format(name,email))
    exist = cursor.fetchone() 
    
    if exist is None:
        cursor.execute("""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'lists';""")        
        cursor.execute("""INSERT INTO lists(name,date,email)VALUES('{}','{}','{}');""".format(name,today,email))
        
        connection.commit()
        cursor.close()
        connection.close()
    
    else:
        return ('List already exists!!!')
    
    return "You have created the list '{}' successfully!".format(name)

#Delete list on DB
def deleteList(name):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM lists WHERE name = '{}';""".format(name))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the list '{}' successfully!".format(name)

#Rename list on DB
def updateList(name,idn):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE lists SET name = '{}' WHERE idlist = '{}';""".format(name,idn))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have renamed the list number '{}' to '{}' successfully!".format(idn,name)

#Create task on DB
def createTask(name,idlist,email):
    now = datetime.now()
    today = now.strftime("%Y/%m/%d %H:%M:%S")
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'tasks';""")        
    cursor.execute("""INSERT INTO tasks(name,date,idlistt,email)VALUES('{}','{}','{}','{}');""".format(name,today,idlist,email))
    
    connection.commit()
    cursor.close()
    connection.close()
  
    return "You have created the task '{}' successfully!".format(name)



#Delete all tasks by idlistt
def deltasks(idlist):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM tasks WHERE idlistt = '{}';""".format(idlist))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the tasks successfully!"


#Delete task on DB
def deleteTask(name):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM tasks WHERE name = '{}';""".format(name))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the task '{}' successfully!".format(name)

#Rename task on DB
def updateTask(name,idn):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE tasks SET name = '{}' WHERE idlist = '{}';""".format(name,idn))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have renamed the task number '{}' to '{}' successfully!".format(idn,name)

#Make new Table
def newtable():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
    """CREATE TABLE admin(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(32),
        password VARCHAR(32)
    );"""

    )
    print("Created new table!")
    connection.commit()
    cursor.close()
    connection.close()
#Delete Table
def deltable():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
    """DROP TABLE admin;"""

    )
    print("Dropped table!")
    connection.commit()
    cursor.close()
    connection.close()

