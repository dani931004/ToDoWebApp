from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine
from psycopg2 import Error
from datetime import datetime

db = SQLAlchemy()

now = datetime.now()
today = now.strftime("%Y-%m-%d %H:%M:%S")

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="mxvufuhtwjccvs",
                                  password="0410",
                                  host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com",
                                  port="5432",
                                  database="d2bjsr179tpgef")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
'''finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
'''




class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }



class users(BaseModel, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.String(120), default=datetime.now)
    
class admin(BaseModel, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

class lists(BaseModel, db.Model):
    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.String(120), default=datetime.now)

class tasks(BaseModel, db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.String(120), default=datetime.now)


#Check if password is right
def check_pw(email):
    
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE email like '{}' ORDER BY idUser DESC;""".format(email))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    
    return password

def check_pw_adm(email):
    
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM admin WHERE email = '{}' ORDER BY idAdmin DESC;""".format(email))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    
    return password

#Select usernames signed up in the last 24hours
def last24h():
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT email
                      FROM users
                      WHERE NOW() > datetime::timestamptz
                      AND NOW() - datetime::timestamptz <= interval '24 hours'
                      ORDER BY datetime;""")    
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo


#Select all Lists created in the last 24hours
def last24hLists():
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT name
                    FROM lists
                    WHERE NOW() > date::timestamptz
                    AND NOW() - date::timestamptz <= interval '24 hours'
                    ORDER BY date;""") 
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo


#Total Lists created
def totalLists():
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
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
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
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
    
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
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


#Delete the User, their Lists and their Tasks on DB
def delUser(name):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM users WHERE email = '{}';""".format(name))
    cursor.execute("""DELETE FROM lists WHERE email = '{}';""".format(name))
    cursor.execute("""DELETE FROM tasks WHERE email = '{}';""".format(name))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the user '{}' and all their lists and tasks successfully!".format(name)

#Show all details of a user on DB
def selUser(email):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE email = '{}';""".format(email))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Show all tasks of a user on DB
def allUserTasks(email):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM tasks WHERE email = '{}';""".format(email))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Show all lists of a user on DB
def allUserLists(email):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM lists WHERE email = '{}';""".format(email))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo


#Show all users on DB
def allUsers():
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users;""")
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    return todo

#Select list by ID
def selList(username):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM lists WHERE email = '{}';""".format(username))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return todo

#Select task by ID of list
def selTask(idlist,username):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM tasks WHERE (idList = '{}' and email = '{}');""".format(idlist,username))
    todo = cursor.fetchall()
    
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return todo

#Create list on DB
def createList(name,email):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""SELECT name FROM lists WHERE (name = '{}' and email = '{}');""".format(name,email))
    exist = cursor.fetchone() 
    
    if exist is None:          
        cursor.execute("""INSERT INTO lists(name,date,email)VALUES('{}','{}','{}');""".format(name,today,email))
        
        connection.commit()
        cursor.close()
        connection.close()
    
    else:
        return ('List already exists!!!')
    
    return "You have created the list '{}' successfully!".format(name)

#Delete list on DB
def deleteList(name):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM lists WHERE name = '{}';""".format(name))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the list '{}' successfully!".format(name)

#Rename list on DB
def updateList(name,idn):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""UPDATE lists SET name = '{}' WHERE idList = '{}';""".format(name,idn))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have renamed the list number '{}' to '{}' successfully!".format(idn,name)

#Create task on DB
def createTask(name,idlist,email):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M:%S")
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO tasks(name,date,idList,email)VALUES('{}','{}','{}','{}');""".format(name,today,idlist,email))
    
    connection.commit()
    cursor.close()
    connection.close()
  
    return "You have created the task '{}' successfully!".format(name)



#Delete all tasks by idlistt
def deltasks(idlist):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM tasks WHERE idList = '{}';""".format(idlist))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the tasks successfully!"


#Delete task on DB
def deleteTask(name):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM tasks WHERE name = '{}';""".format(name))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have deleted the task '{}' successfully!".format(name)

#Rename task on DB
def updateTask(name,idn):
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute("""UPDATE tasks SET name = '{}' WHERE idTask = '{}';""".format(name,idn))
        
    connection.commit()
    cursor.close()
    connection.close()
    
    return "You have renamed the task number '{}' to '{}' successfully!".format(idn,name)

#Make new Table
def newtable():
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute(
    """CREATE TABLE admin(
        idAdmin INTEGER PRIMARY KEY AUTOINCREMENT,
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
    connection = psycopg2.connect(database="d2bjsr179tpgef", user="mxvufuhtwjccvs",password="0410", host="ec2-99-81-238-134.eu-west-1.compute.amazonaws.com", port="5432")
    cursor = connection.cursor()
    cursor.execute(
    """DROP TABLE admin;"""

    )
    print("Dropped table!")
    connection.commit()
    cursor.close()
    connection.close()

