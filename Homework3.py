from flask import Flask, render_template, request, session, redirect, url_for, g
import model

app = Flask(__name__)
app.secret_key = 'jumpjacks'

username = ''

user = model.check_users()

idList=1

@app.route("/", methods = ["GET"])
def home():
  if 'email' in session:
    g.user=session['email']
    todolist = model.selList(username)
    return render_template('dashboard.html', message = 'Welcome to Dashboard! {}'.format(username), todolist = todolist)
  return render_template('homepage.html', message = 'Log in to the page or sign up!')
  
@app.route('/adminpage', methods = ['GET'])
def adminpage():
  if 'email' in session:
    g.user=session['email']
    return render_template('adminpage.html', message = 'Welcome to Adminpage! {}'.format(username))
  return render_template('admin.html')

@app.before_request
def before_request():
  g.email = None
  if 'email' in session:
    g.email = session['email']
    

@app.route('/login', methods= ['GET','POST'])
def login():
  global username
  if request.method ==  'POST':
    session.pop('email', None)
    username = request.form['email']
    pwd = model.check_pw(username)
    if request.form['password'] == pwd:
      session['email'] = request.form['email']
      return redirect(url_for('home'))
  return render_template('login.html')


@app.route('/getsession')
def getSession():
  if 'email' in session:
    return session['email']
  return redirect(url_for('login'))

@app.route('/logout')
def logout():
  session.pop('email', None)
  return redirect(url_for('home'))

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
    global username
    if request.method ==  'POST':
      session.pop('email', None)
      username = request.form['email']
      pwd = model.check_pw_adm(username)
      if request.form['password'] == pwd:
        session['email'] = request.form['email']
        return redirect(url_for('adminpage'))
    return render_template('admin.html')




@app.route('/aboutus', methods= ['GET'])
def about():
  return render_template('aboutus.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
  if 'email' in session:
    g.user=session['email']
    todolist = model.selList(username)
    return render_template('dashboard.html', message = 'Welcome to Dashboard {}'.format(username), todolist=todolist)
  message = "Log in to the page or sign up!"
  return render_template('homepage.html', message = message)

        
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  dbadd = model.createList(name,username)
  todolist = model.selList(username)
  return render_template('dashboard.html', message = dbadd, todolist = todolist)

@app.route('/dell', methods=['POST'])  
def dell():
  name = request.form['name']
  idlist = request.form['idlistt']
  dbdell = model.deleteList(name)
  todolist = model.selList(username)
  deltasks = model.deltasks(idlist)
  return render_template('dashboard.html', message = dbdell, todolist = todolist)

@app.route('/update', methods = ['POST'])
def update():
  name = request.form["name"]
  number = request.form["number"]
  dbupdate = model.updateList(name,number)
  todolist = model.selList(username)
  return render_template('dashboard.html',message = dbupdate, todolist = todolist)



@app.route('/todolist', methods= ['GET','POST'])
def todolist():
  global idList
  idlist = request.form['idlist'] # ID of the List
  idList = idlist
  listname = request.form['listname']
  alltasks = model.selTask(idlist,username)
  sellist = model.selList(username)
  return render_template('todolist.html',listname = listname, idlist = idlist, alltasks = alltasks, sellist=sellist),idList

@app.route('/addtask', methods= ['POST'])
def addtask():
  name = request.form['name']
  idlistt = request.form['idlistt']
  dbadd = model.createTask(name,idList,username)
  sellist = model.selList(username)
  alltasks = model.selTask(idList,username)
  return render_template('todolist.html',idlistt = idlistt, message = dbadd, alltasks = alltasks, sellist = sellist)


@app.route('/updatetask', methods= ["POST"])
def updatetask():
  number = request.form["number"]
  name = request.form["name"]
  dbupdate = model.updateTask(name,number)
  sellist = model.selList(username)
  alltasks = model.selTask(idList,username)
  return render_template('todolist.html', alltasks = alltasks, sellist = sellist)

@app.route('/deltask', methods= ['POST'])
def deltask():
  name = request.form["name"]
  dbdel = model.deleteTask(name)
  idlistt = request.form['idlistt']
  alltasks = model.selTask(idList,username)
  sellist = model.selList(username)
  return render_template('todolist.html',sellist = sellist, message = dbdel,alltasks = alltasks)

@app.route('/privacy', methods= ['GET'])
def privacy():
  return render_template('privacy.html')

@app.route('/termsofuse', methods= ['GET'])
def termsofuse():
  return render_template('termsofuse.html')



if __name__ == "__main__":
  app.run(host="192.168.0.110",debug = True)
