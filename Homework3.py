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
    todolist = model.allLists()
    return render_template('dashboard.html', message = 'Welcome to Dashboard!', todolist = todolist)
  return render_template('homepage.html', message = 'Log in to the page or sign up!')
  


@app.before_request
def before_request():
  g.email = None
  if 'email' in session:
    g.email = session['email']
    

@app.route('/login', methods= ['GET','POST'])
def login():
  if request.method ==  'POST':
    session.pop('email', None)
    areyouuser = request.form['email']
    pwd = model.check_pw(areyouuser)
    if request.form['password'] == pwd:
      session['email'] = request.form['email']
      return redirect(url_for('home'))
  return render_template('index.html')


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
    message = "Please sign up!"
    return render_template('signup.html', message = message)
  else:
    email = request.form["email"]
    password = request.form["password"]
    message = model.signup(email, password)
    return render_template('signup.html',message = message)
    

@app.route('/aboutus', methods= ['GET'])
def about():
  return render_template('aboutus.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
  return render_template('dashboard.html')
        
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  dbadd = model.createList(name)
  todolist = model.allLists()
  return render_template('dashboard.html', message = dbadd, todolist = todolist)

@app.route('/dell', methods=['POST'])  
def dell():
  name = request.form['name']
  idlist = request.form['idlistt']
  dbdell = model.deleteList(name)
  todolist = model.allLists()
  deltasks = model.deltasks(idlist)
  return render_template('dashboard.html', message = dbdell, todolist = todolist)

@app.route('/update', methods = ['POST'])
def update():
  name = request.form["name"]
  number = request.form["number"]
  dbupdate = model.updateList(name,number)
  todolist = model.allLists()
  return render_template('dashboard.html',message = dbupdate, todolist = todolist)



@app.route('/todolist', methods= ['GET','POST'])
def todolist():
  global idList
  idlist = request.form['idlist'] # ID of the List
  idList = idlist
  alltasks = model.selTask(idlist)
  sellist = model.selList(idlist)
  return render_template('todolist.html',idlist = idlist, alltasks = alltasks, sellist=sellist),idList

@app.route('/addtask', methods= ['POST'])
def addtask():
  name = request.form['name']
  idlistt = request.form['idlistt']
  dbadd = model.createTask(name,idList)
  sellist = model.selList(idList)
  alltasks = model.selTask(idList)
  return render_template('todolist.html',idlistt = idlistt, message = dbadd, alltasks = alltasks, sellist = sellist)


@app.route('/updatetask', methods= ["POST"])
def updatetask():
  number = request.form["number"]
  name = request.form["name"]
  dbupdate = model.updateTask(name,number)
  sellist = model.selList(idList)
  alltasks = model.selTask(idList)
  return render_template('todolist.html', alltasks = alltasks, sellist = sellist)

@app.route('/deltask', methods= ['POST'])
def deltask():
  name = request.form["name"]
  dbdel = model.deleteTask(name)
  idlistt = request.form['idlistt']
  alltasks = model.selTask(idList)
  sellist = model.selList(idList)
  return render_template('todolist.html',sellist = sellist, message = dbdel,alltasks = alltasks)

@app.route('/privacy', methods= ['GET'])
def privacy():
  return render_template('privacy.html')

@app.route('/termsofuse', methods= ['GET'])
def termsofuse():
  return render_template('termsofuse.html')



if __name__ == "__main__":
  app.run(host="192.168.0.110",debug = True)
