from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'god'
 
mysql = MySQL(app)


# this is for login
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM good WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('new.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

# this is for logout
 
@app.route('/logout') 
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# this is for registration
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM good WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO good VALUES (% s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

# this is for home

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        uc = request.form
        name = uc['name-p']
        date = uc['date']
        time = uc['time']
        card_n = uc['card']
        doctor = uc['name-d']
        cursor  = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO buyer VALUES(%s, %s, %s, %s, %s)', (name, date, time, card_n, doctor))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/index', methods=['GET'])
def index():
       k = mysql.connection.cursor()
       data = k.execute('SELECT * FROM buyer')
       if data > 0:
           uc = k.fetchall()
           return render_template('index.html', uc = uc)
       
#@app.route('/delete', methods=[''])
#def delete(): 
   


if __name__ == '__main__':
    app.run(debug=True)