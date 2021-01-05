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

#Sign up the user
def signup(email, password):
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE email = '{}';""".format(email))
    exist = cursor.fetchone() 
    
    if exist is None:
        cursor.execute("""INSERT INTO users(email,password)VALUES('{}', '{}');""".format(email,password))
        
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
    cursor.execute("""SELECT email FROM users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    users = []
    
    
    for i in range((len(db_users))):
        person = db_users[i][0]
        users.append(person)
    
    
    
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return users

#Show all lists on DB
def allLists():
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM lists;""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Create list on DB
def createList(name):
    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    connection = sqlite3.connect('/home/dani/Desktop/Python3/Flask/Homework3/todo.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT name FROM lists WHERE name = '{}';""".format(name))
    exist = cursor.fetchone() 
    
    if exist is None:
        cursor.execute("""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'lists';""")        
        cursor.execute("""INSERT INTO lists(name,date)VALUES('{}','{}');""".format(name,today))
        
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
    cursor.execute("""UPDATE lists SET name = '{}' WHERE pk = '{}';""".format(name,idn))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have renamed the list number '{}' to '{}' successfully!".format(idn,name)

