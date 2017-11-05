from flask import Flask,render_template,session,request,jsonify,json,redirect,url_for
from hashlib import md5
import MySQLdb

cus_info = "Hello"
emp_info = ""
addr_info = ""
app = Flask(__name__)
app.secret_key = "aw456787uioSHUI4w5eQuighepuihqetoghRUIGHQEOh"

db = MySQLdb.connect("localhost","root","aish1234","hsh" )
cur = db.cursor()


@app.route("/register")
def register():
	return render_template('register.html')

@app.route("/reg",methods=['POST'])
def reg():
	fname = request.form["f_name"]
	mname = request.form["m_name"]
	lname = request.form["l_name"]
	mail = request.form["email_id"]
	cont = int(request.form["contact"])
	building = request.form["building"]
	street = request.form["street"]
	city = request.form["city"]
	state = request.form["state"]
	password = request.form["password"]
	cur.execute("INSERT INTO Name(first_name,middle_name,last_name) VALUES (%s,%s,%s)",(fname,mname,lname))
	db.commit()
	cur.execute("INSERT INTO Address(building_name,street_name,city,state) VALUES (%s,%s,%s,%s)",(building,street,city,state))
	db.commit()
	cur.execute("SELECT name_id FROM Name where first_name = %s and middle_name = %s and last_name = %s",(fname,mname,lname))
	nameid=int(cur.fetchone()[0])
	cur.execute("SELECT addr_id FROM Address where building_name = %s and street_name = %s and city = %s and state = %s",(building,street,city,state))
	addrid=int(cur.fetchone()[0])
	cur.execute("INSERT INTO Customer(password,cus_name_id,cus_email_id,addr_id) VALUES (%s,%s,%s,%s)",(password,nameid,mail,addrid))
	cur.execute("SELECT cus_id FROM Customer where cus_name_id = %s and addr_id = %s",(nameid,addrid))
	cusid=int(cur.fetchone()[0])
	cur.execute("INSERT INTO Customer_contact VALUES (%s,%s)",(cusid,cont))
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
		cur.execute("SELECT * FROM Customer WHERE cus_id = %s",[userkey]);
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM Customer where cus_id = %s",[userkey]);
			for row in cur.fetchall():
				if md5(passkey).hexdigest() == row[0]:
					session['username'] = request.args.get['username']
					cus_info = userkey
					cus_info = int(cus_info)
					return render_template("index.html")
				else:
					error = "Invalid Credential"
		else:
			error = "Invalid Credential"
		return render_template('index.html', error=error)
	except Exception as e:
		return render_template("login.html",error=e)

@app.route("/")
@app.route("/home")
def home():
	return render_template("login.html")

@app.route("/appliance")
def appliance():
	cus_info = session.get("username")
	return render_template("appliances.html?username="+cus_info)

@app.route("/added", methods=['POST'])
def added():
	aname = request.form["a_name"]
	wdate = request.form["w_date"]
	wduration = int(request.form["w_duration"])
	currentstate = request.form["cur_state"]
	cur.execute("INSERT INTO Appliance(cus_id,appliance_name,warranty_start_date, warranty_duration, current_state) VALUES (%s,%s,%s,%s,%s)",(session['cus_id']	,aname, wdate,wduration,currentstate))
	db.commit()
	return render_template('addappliance.html')

@app.route("/add_app")
def add_app():
	return render_template("addappliance.html")

@app.route("/del_app")
def del_app():
	return render_template("delappliance.html")

@app.route("/ctrl_app")
def ctrl_app():
	return render_template("ctrlappliance.html")

@app.route("/rep_app")
def rep_app():
	return render_template("repappliance.html")

# @app.route("/elec")
# def elec():
# 	return render_template("electricity.html")

# @app.route("/perinfo")
# def perinfo():
# 	return render_template("personalinfo.html")

@app.route("/comp")
def comp():
	return render_template("complaint.html")

@app.route("/about")
def about():
	return render_template("aboutus.html")

@app.route("/contact")
def contact():
	return render_template("contactus.html")


if __name__ == '__main__':
	app.run(debug=True)