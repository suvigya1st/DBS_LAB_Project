import traceback, warnings
import requests
warnings.filterwarnings("ignore")

from flask import Flask, render_template, json, request, session, redirect, make_response, jsonify, escape
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import datetime
import smtplib
import pytz

tz_timezone = pytz.timezone('Asia/Kolkata')

mysql = MySQL()
app = Flask(__name__)
# MySQL configurations


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'smoked'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/leaderboard')
def leaderboard():
	if(session.get('user')):
		try:
			conn=mysql.connect()
			try:
				cursor=conn.cursor()
				cursor.execute("SELECT user_name FROM `tbl_user` ORDER BY `current_level` DESC, `time_stamp` LIMIT 10")
				#select user_name from 'tbl_user' order by 'level' desc, 'time_stamp' limit 10
			except:
				message="Couldnt query the database"
				return dataFormatter(404,message,[])
			data = cursor.fetchall() 
			players = []

			for row in data:
				user={}
				user['name']=row[0];
				players.append(user)
		
			message = "Success. Found "+str(len(players))+" players."
			return render_template("leaderboard.html",players=players)
		except Exception as e:
			message = "Database connection could not be established" + str(e)
			return dataFormatter(404,message,[])
		finally:
			conn.close();
	else:
		return redirect('/signin')
