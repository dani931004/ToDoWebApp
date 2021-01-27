import sqlite3

connection = sqlite3.connect('https://github.com/dani931004/Homework3/blob/main/todo.db', check_same_thread = False)
cursor = connection.cursor()

#Tables
#Table 1 'users' columns:['email', 'pass'] V
#Table 2 'lists' columns:['name', 'date']
#Table 3 'tasks' columns:['name', 'date', 'time']
cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(32),
        password VARCHAR(32)
    );"""

)



cursor.execute(
    """CREATE TABLE lists(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(16),
        date VARCHAR(16)
    );"""

)



cursor.execute(
    """CREATE TABLE tasks(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(16),
        date VARCHAR(16),
        time VARCHAR(16)
    );"""

)
connection.commit()
cursor.close()
connection.close()

