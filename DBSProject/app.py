from flask import Flask,render_template,session,request,jsonify,json,redirect,url_for
from hashlib import md5
import MySQLdb

app = Flask(__name__)
app.secret_key = "aw456787uioSHUI4w5eQuighepuihqetoghRUIGHQEOh"

db = MySQLdb.connect("localhost","root","password","test")
cur = db.cursor()


@app.route("/")
def register():
	return render_template('register.html')

@app.route("/reg",methods=['POST'])
def reg():
	fname = request.form["f_name"]
	mail = request.form["email_id"]
	cur.execute("INSERT INTO register(name,email) VALUES (%s,%s)",(fname,mail))
	db.commit()
	return render_template('login.html')

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/login_test", methods=['GET'])
def login_test():
	userkey = request.args.get("username")
	passkey = request.args.get("password")
	try:
		error = None
		cur.execute("SELECT * FROM login WHERE username = %s",[userkey]);
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM login where username = %s",[userkey]);
			for row in cur.fetchall():
				if md5(passkey).hexdigest() == row[0]:
					session['username'] = request.form['username']
					return redirect(url_for('index'))
				else:
					error = "Invalid Credential"
		else:
			error = "Invalid Credential"
		return render_template('index.html', error=error)
	except Exception as e:
		return render_template("login.html")

@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("aboutus.html")

@app.route("/contact")
def contact():
	return render_template("contactus.html")

if __name__ == '__main__':
	app.run(debug=True)