from ast import Pass
from telnetlib import STATUS
from unicodedata import name
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import pymysql
pymysql.install_as_MySQLdb()
from flask_cors import CORS, cross_origin
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL, MySQLdb
from sre_constants import SUCCESS
from flask import Flask, render_template, request, flash, redirect
from flask import *
import re
from mysql.connector import Error


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
CORS(app, support_credentials=True)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ayesha'
app.config['MYSQL_DB'] = 'personsite'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)





@app.route('/')
def main():
    return (render_template('main.html'))

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('main'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
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
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
   
@app.route('/home', methods=['GET','POST'])
def home():
    return (render_template('home.html'))

@app.route('/completed', methods=['GET','POST'])
def completed():
    name = request.form.get("name")
    gender = request.form.get("gender")
    age = request.form.get("age")
    #date = request.form.get("date")
    seen = request.form.get("seen")
    height = request.form.get("height")
    weight = request.form.get("weight")
    marks = request.form.get("marks")
    comp = request.form.get("comp")
	#status = request.form.get("status")
	

    cur = mysql.connection.cursor()
    print(name,gender,age,seen,height,weight,marks,comp,)
    cur.execute(
        "INSERT INTO data(name,gender,age,seen,height,weight,marks,comp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (name,gender,age,seen,height,weight,marks,comp,))
	
    mysql.connection.commit()
    cur.close()
    return render_template("completed.html",name=name, gender=gender,age=age,seen=seen,height=height,weight=weight,marks=marks,comp=comp,)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
@app.route('/projectlist',methods=['GET','POST'])
def projectlist():
    #creating variable for connection
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #executing query
    cursor.execute("select * from data")
    #fetching all records from database
    data=cursor.fetchall()
    #returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("projectlist.html",data=data)

      
@app.route('/page1')
def page1():
    return (render_template('page1.html'))

@app.route('/found')
def found():
    return (render_template('found.html'))

@app.route('/completed1',methods=['GET','POST'])
def completed1():
	
		status = request.form.get("status")
		id = request.form.get("id")
		#data=0
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#cursor1=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#sql_select_query="""select id from data where name =%s"""
		#cursor1.execute(sql_select_query,name)
	    #data=cursor1.fetchall()
	
			
		sql_update_query = """Update data set status = %s where id = %s"""
		input_data = (status, id)
		cursor.execute(sql_update_query, input_data)

		mysql.connection.commit()
    	
		return(render_template('completed1.html'))
    

	
@app.route('/directory',methods=['GET','POST'])
def directory():
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   
    cursor.execute("select id,name,status from data")
    
    data=cursor.fetchall()
    
    return render_template("directory.html",data=data)

    


if __name__=="__main__":
    app.run(debug=True)