from flask import Flask, render_template, request, session, redirect, url_for, g
import model

app = Flask(__name__)
app.secret_key = 'jumpjacks'

username = ''
user = model.check_users()



@app.route("/", methods = ["GET"])
def home():
  if 'email' in session:
    g.user=session['email']
    return render_template('dashboard.html', message = 'You are logged in!')
  return render_template('homepage.html', message = 'Log in to the page or sign up!')
  
""" @app.route("/delete", methods = ["GET"])
def delete():
  name = request.form["name"]
  message = model.deleteList(name)
  return render_template('dashboard.html',message = message) """

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

@app.route('/dashboard', methods= ['GET','POST'])
def dashboard():
  if request.method == 'GET':
    message = "Welcome to Dashboard!"
    return render_template('dashboard.html', message = message)
  else:
    todos = model.all()
    return render_template('dashboard.html', todos=todos)
      
    
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  dbadd = model.createList(name)
  return render_template('dashboard.html', message = dbadd)
    

@app.route('/list', methods= ['GET'])
def list():
  return render_template('list.html')

@app.route('/privacy', methods= ['GET'])
def privacy():
  return render_template('privacy.html')

@app.route('/termsofuse', methods= ['GET'])
def termsofuse():
  return render_template('termsofuse.html')


if __name__ == "__main__":
  app.run(host="192.168.0.110",debug = True)
