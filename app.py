from flask import Flask, render_template, request, session, redirect, url_for, g, make_response
import flask
import model
from flask_paginate import Pagination, get_page_parameter, get_page_args
from model import db


SQLALCHEMY_DATABASE_URI = "postgres://mxvufuhtwjccvs:b11b3a25eacaedf50b69fd4e70b830fc4e0ae64a60101ce7fca2109740ee61b5@ec2-99-81-238-134.eu-west-1.compute.amazonaws.com:5432/d2bjsr179tpgef"
#app name
app = Flask(__name__)



# app config
db.init_app(app)
app.secret_key = "daniconda"
users = list(range(len(model.allUsers())))

user = model.check_users()

@app.route("/", methods = ["GET"])
def home():
  if 'email' in session:
    g.user=session['email']
    todolist = model.selList(g.user)
    return render_template('dashboard.html', message = 'Welcome to Dashboard! {}'.format(g.user), todolist = todolist)
  return render_template('homepage.html', message = 'Log in to the page or sign up!')
  
@app.route('/adminpage', methods = ['GET'])
def adminpage():
  if 'email' in session and (session['email'] == "admin"):
    g.user=session['email']
    allusers = model.allUsers()
    last24 = model.last24h()
    totalLists = model.totalLists()
    lists24 = model.last24hLists()
    return render_template('adminpage.html',lists24=lists24,totalLists = totalLists, last24=last24, allusers = allusers, message = 'Welcome to Adminpage! {}'.format(g.user))
  
  return render_template('admin.html')

@app.before_request
def before_request():
  g.email = None
  if 'email' in session:
    g.email = session['email']
    

username = ""
@app.route('/login', methods= ['GET','POST'])
def login():
  global username
  if request.method ==  'POST':
    session.pop('email', None)
    username = request.form['email']
    todolist = model.selList(username)
    res = make_response(render_template('dashboard.html', todolist = todolist))
    res.set_cookie('email', username)
    pwd = model.check_pw(username)
    if request.form['password'] == pwd:
      session['email'] = request.form['email']
      return res
  return render_template('login.html')


@app.route('/getsession')
def getSession():
  if 'email' in session:
    return session['email']
  return redirect(url_for('login'))

@app.route('/logout')
def logout():
  session.pop('email', None)
  res = make_response(render_template('homepage.html'))
  res.set_cookie('email', username, max_age = 0)
  
  return res

@app.route('/signup', methods= ['GET','POST'])
def signup():
  if request.method == 'GET':
    message = "Please sign up"
    return render_template('signup.html', message = message)
  else:
    email = request.form["email"]
    password = request.form["password"]
    message = model.signup(email, password)
    return render_template('signup.html',message = message)

@app.route('/getsessionadm')
def getSessionadm():
  if 'email' in session:
    return session['email']
  return redirect(url_for('admin'))



@app.route('/admin', methods = ['GET', 'POST'])
def admin():
  if request.method ==  'POST':
    session.pop('email', None)
    username = request.form['email']
    pwd = model.check_pw_adm(username)
    if request.form['password'] == pwd:
      session['email'] = request.form['email']
      return redirect(url_for('adminpage'))
  return render_template('admin.html')




@app.route('/userspage', methods = ['GET','POST'])
def userspage():
  if 'email' in session and (session['email'] == "admin"):
    per_page = request.args.get(key="",type=int, default=50)
    allusers = model.allUsers()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page
    total = len(model.allUsers())
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('userspage.html',allusers=allusers, users=pagination_users, page=page, per_page=per_page, pagination=pagination)
  return render_template('admin.html')


@app.route('/userinfo', methods = ['GET','POST'])
def userinfo():
  userinfo = request.form['email']
  user = model.selUser(userinfo)
  for i in user:
    email = i
  lists = model.selList(userinfo)
  return render_template('userinfo.html', lists = lists, user = email)


@app.route('/deluser', methods = ['GET','POST'])
def deluser():
  name = request.form['name']
  user = model.selUser(name)
  for i in user:
    email = i
  lists = model.selList(name)
  message = model.delUser(name)
  return render_template('userinfo.html', message =  message, lists = lists, user = email)


def get_users(offset=0, per_page=50):
  return users[offset: offset + per_page]


@app.route('/aboutus', methods= ['GET'])
def about():
  return render_template('aboutus.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
  if 'email' in session:
    username = request.cookies.get('email')
    g.user=session['email']
    todolist = model.selList(username)
    return render_template('dashboard.html', message = 'Welcome to Dashboard {}'.format(username), todolist=todolist)
  message = "Log in to the page or sign up!"
  return render_template('homepage.html', message = message)

        
@app.route('/add', methods=['POST'])
def add():
  username = request.cookies.get('email')
  name = request.form['name']
  dbadd = model.createList(name,username)
  todolist = model.selList(username)
  return render_template('dashboard.html', message = dbadd, todolist = todolist)

@app.route('/dell', methods=['POST'])  
def dell():
  if 'email' in session:
    username = request.cookies.get('email')
    name = request.form['name']
    idlist = request.form['idlistt']
    dbdell = model.deleteList(name)
    todolist = model.selList(username)
    deltasks = model.deltasks(idlist)
    return render_template('dashboard.html', message = dbdell, todolist = todolist)
  else:
    return render_template('homepage.html')
@app.route('/update', methods = ['POST'])
def update():
  username = request.cookies.get('email')
  name = request.form["name"]
  number = request.form["number"]
  dbupdate = model.updateList(name,number)
  todolist = model.selList(username)
  return render_template('dashboard.html',message = dbupdate, todolist = todolist)


idList = ""
@app.route('/todolist', methods= ['GET','POST'])
def todolist():
  global idList
  username = request.cookies.get('email')
  idlist = request.form['idlist'] # ID of the List
  idList = idlist
  listname = request.form['listname']
  alltasks = model.selTask(idlist,username)
  sellist = model.selList(username)
  return render_template('todolist.html',listname = listname, idlist = idlist, alltasks = alltasks, sellist=sellist)

@app.route('/addtask', methods= ['POST'])
def addtask():
  username = request.cookies.get('email')
  name = request.form['name']
  idlistt = request.form['idlistt']
  dbadd = model.createTask(name,idList,username)
  sellist = model.selList(username)
  alltasks = model.selTask(idList,username)
  return render_template('todolist.html',idlistt = idlistt, message = dbadd, alltasks = alltasks, sellist = sellist)


@app.route('/updatetask', methods= ["POST"])
def updatetask():
  username = request.cookies.get('email')
  number = request.form["number"]
  name = request.form["name"]
  idlistt = request.form['idlistt']
  dbupdate = model.updateTask(name,number)
  sellist = model.selList(username)
  alltasks = model.selTask(idList,username)
  return render_template('todolist.html', idlistt = idlistt, alltasks = alltasks, sellist = sellist)

@app.route('/deltask', methods= ['POST'])
def deltask():
  username = request.cookies.get('email')
  name = request.form["name"]
  dbdel = model.deleteTask(name)
  idlistt = request.form['idlistt']
  alltasks = model.selTask(idList,username)
  sellist = model.selList(username)
  return render_template('todolist.html', idlistt = idlistt, sellist = sellist, message = dbdel, alltasks = alltasks)

@app.route('/privacy', methods= ['GET'])
def privacy():
  return render_template('privacy.html')

@app.route('/termsofuse', methods= ['GET'])
def termsofuse():
  return render_template('termsofuse.html')



if __name__ == "__main__":
  app.run()
