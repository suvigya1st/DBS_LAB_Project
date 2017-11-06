from flask import Flask,render_template,session,request,jsonify,json,redirect,url_for
from hashlib import md5
import MySQLdb

cus_info = "Hello"
emp_info = ""
addr_info = ""
app = Flask(__name__)
app.secret_key = "aw456787uioSHUI4w5eQuighepuihqetoghRUIGHQEOh"

db = MySQLdb.connect("localhost","root","password","hsh2" )


@app.route("/register")
def register():
	return render_template('register.html')


@app.route("/reg",methods=['GET','POST'])
def reg():
	if not session.get('cusid'):	
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
		cur = db.cursor()
		cur.execute("INSERT INTO Name(first_name,middle_name,last_name) VALUES (%s,%s,%s)",(fname,mname,lname))
		db.commit()
		nameid = cur.lastrowid
		cur.execute("INSERT INTO Address(building_name,street_name,city,state) VALUES (%s,%s,%s,%s)",(building,street,city,state))
		db.commit()
		addrid = cur.lastrowid
		# cur.execute("SELECT name_id FROM Name where first_name = %s and middle_name = %s and last_name = %s",(fname,mname,lname))
		# nameid=int(cur.fetchone()[0])
		# cur.execute("SELECT addr_id FROM Address where building_name = %s and street_name = %s and city = %s and state = %s",(building,street,city,state))
		# addrid=int(cur.fetchone()[0])
		cur.execute("INSERT INTO Customer(password,cus_name_id,cus_email_id,addr_id) VALUES (%s,%s,%s,%s)",(password,nameid,mail,addrid))
		cusid = cur.lastrowid


		# cur.execute("SELECT cus_id FROM Customer where cus_name_id = %s and addr_id = %s",(nameid,addrid))
		# cusid=int(cur.fetchone()[0])
		cur.execute("INSERT INTO Customer_contact VALUES (%s,%s)",(cusid,cont))
		db.commit()
		print cusid
		return render_template('login.html',cusid = cusid)
	else:
		return redirect("/index")

@app.route("/")
@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/login_test", methods=['POST'])
def login_test():
	userkey = request.form["username"]
	passkey = request.form["password"]
	try:
		error = None
		cur = db.cursor()
		print 1
		cur.execute("SELECT * FROM Customer WHERE cus_id = %s" %userkey);
		print 3
		if cur.fetchone():
			print 4
			cur.execute("SELECT password FROM Customer where cus_id = %s",[userkey]);
			for row in cur.fetchall():	
				print 2
				if passkey == row[0]:
					session['cusid'] = userkey
					print "loggedin" 
					print session['cusid']
					return render_template("index.html",cusid = userkey)
				else:
					error = "Wrong Password"
					print error
					return render_template('login.html', error=error)
		else:
			error = "User Not Registered"
			print "error"
			return render_template('login.html', error=error)
	except Exception as e:
		print e
		return render_template("login.html",error=e)

@app.route("/index")
def index():
	return render_template("index.html",cusid=session['cusid'])

@app.route("/home")
def home():
	return render_template("index.html",cusid=session['cusid'])

@app.route("/appliance")
def appliance():
	if session.get("cusid"):
		return render_template("appliances.html",cusid=session['cusid'])
	else:
		return redirect("/login")

@app.route("/added", methods=['POST'])
def added():
	try:
		aname = request.form["a_name"]
		wdate = request.form["w_date"]
		wduration = int(request.form["w_duration"])
		currentstate = request.form["cur_state"]
		try:
			cur = db.cursor()
			try:
				print session.get('cusid')
				cur.execute("INSERT INTO Appliance(cus_id,appliance_name,warranty_start_date, warranty_duration, current_state) VALUES (%s,%s,%s,%s,%s)",(session.get("cusid"),aname, wdate,wduration,currentstate))
				db.commit()
				return render_template('appliances.html', error="Added")
			except Exception as e:
				return render_template('addappliance.html', error = e)
		except Exception as e:
			print e
			return "Could not connect to database"
	except Exception as e:
		return "Form values not submitted properly."

@app.route("/add_app")
def add_app():
	return render_template("addappliance.html",cusid=session['cusid'])

@app.route("/del_app")
def del_app():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print "IN DELETE APPLIANCE"
		print appl_li
		return render_template("delappliance.html",cusid=session['cusid'],del_app_li = appl_li)
	except Exception as e:
		print e
		return render_template('appliances.html', error = e)
	
@app.route("/deleted", methods=['POST'])
def deleted():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))

		appl_li = cur.fetchall()
		print "IN DELETED APPLIANCE"
		print appl_li
		del_app_li =  request.form.getlist("del_app_li[]")
		for i in range(len(del_app_li)):
			del_app_li[i] = int(del_app_li[i])
		print del_app_li
		for i in del_app_li:
			cur.execute("DELETE FROM Appliance WHERE cus_id = %s and appliance_id = %s" %(session['cusid'],i))
		db.commit()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li

		return render_template('appliances.html',cusid=session['cusid'] , error ="Deleted")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'], error = e)

@app.route("/ctrl_app")
def ctrl_app():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li
		return render_template("ctrlappliance.html",cusid=session['cusid'],del_app_li = appl_li)
	except Exception as e:
		print e
		return render_template('appliances.html', error = e)

@app.route("/controled", methods=['POST'])
def controled():
	try:
		cur = db.cursor()
		new_app_li = request.form.getlist("ctrl_app_li[]")
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		prev_app_li = cur.fetchall()
		print "ORIGINAL"
		print prev_app_li
		print "MODIFIED"
		for i in range(len(new_app_li)):
			new_app_li[i] = int(new_app_li[i])
		appl_li = {int(i[0]):i[2] for i in prev_app_li}
		for i in appl_li.keys():
			if (i in new_app_li) and (appl_li[i]=='off'):
				# UPDATE that application current_state to 'on'
				cur.execute("UPDATE Appliance SET current_state = %s WHERE appliance_id = %s" ,('on',i))
			elif (i not in new_app_li) and (appl_li[i]=='on'):
				#UPDATE that application current_state to 'off'

				cur.execute("UPDATE Appliance SET current_state = %s WHERE appliance_id = %s" ,('off',i))
		db.commit()

		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li
		return render_template('appliances.html',cusid=session['cusid'],error="Controlled")
	except Exception as e:
		print e
		return render_template('appliances.html',cusid = session['cusid'],error=e)

@app.route("/status_app")
def status_app():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li
		return render_template("statusappliance.html",cusid=session['cusid'],status_app_li = appl_li)
	except Exception as e:
		print e
		return render_template('appliances.html', error = e)

@app.route("/logout")
def logout():
	session.pop("cusid",None)
	return redirect("/")



@app.route("/perinfo")
def perinfo():
	return render_template("personalinfo.html",cusid=session['cusid'])

@app.route("/name")
def name():
	return render_template("nameupdate.html",cusid=session['cusid'])

@app.route("/nameupd", methods=['POST'])
def nameupd():
	try:
		fname = request.form["f_name"]
		mname = request.form["m_name"]
		lname = request.form["l_name"]
		cusid = session['cusid']
		cur = db.cursor()
		cur.execute("SELECT cus_name_id FROM Customer WHERE cus_id = %s" %cusid)
		db.commit()
		nameid = int(cur.fetchone()[0])
		if fname != "":
			cur.execute("UPDATE Name SET first_name = %s WHERE name_id = %s",(fname,nameid))
			db.commit()
		if mname != "":
			cur.execute("UPDATE Name SET middle_name = %s WHERE name_id = %s",(mname,nameid))
			db.commit()
		if lname != "":
			cur.execute("UPDATE Name SET last_name = %s WHERE name_id = %s",(lname,nameid))
			db.commit()
		return render_template('personalinfo.html',cusid = session['cusid'],error="Updated")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)

@app.route("/address")
def address():
	return render_template("addressupdate.html",cusid=session['cusid'])

@app.route("/addressupd", methods=['POST'])
def addressupd():
	try:
		building = request.form["building"]
		street = request.form["street"]
		city = request.form["city"]
		state = request.form["state"]
		cusid = session['cusid']
		cur = db.cursor()
		cur.execute("SELECT addr_id FROM Customer WHERE cus_id = %s" %cusid)
		db.commit()
		addrid = int(cur.fetchone()[0])
		if building != "":
			cur.execute("UPDATE Address SET building_name = %s WHERE addr_id = %s",(building,addrid))
			db.commit()
		if street != "":
			cur.execute("UPDATE Address SET street_name = %s WHERE addr_id = %s",(street,addrid))
			db.commit()
		if city != "":
			cur.execute("UPDATE Address SET city = %s WHERE addr_id = %s",(city,addrid))
			db.commit()
		if state != "":
			cur.execute("UPDATE Address SET state = %s WHERE addr_id = %s",(state,addrid))
			db.commit()
		return render_template('personalinfo.html',cusid = session['cusid'],error="Updated")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)


@app.route("/cont")
def cont():
	return render_template("contactupdate.html",cusid=session['cusid'])

@app.route("/contactupd", methods=['POST'])
def contactupd():
	try:
		cont = int(request.form["contact"])
		cusid = session['cusid']
		cur = db.cursor()
		if cont != "":
			cur.execute("INSERT INTO Customer_contact(cus_id,cus_contact_no) VALUES(%s,%s)",(cusid,cont))
			db.commit()
		return render_template('personalinfo.html',cusid = session['cusid'],error="Updated")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)


@app.route("/email")
def email():
	return render_template("emailupdate.html",cusid=session['cusid'])

@app.route("/emailupd", methods=['POST'])
def emailupd():
	try:
		mail = request.form["email_id"]
		cusid = session['cusid']
		cur = db.cursor()
		if mail != "":
			cur.execute("UPDATE Customer SET cus_email_id = %s WHERE cus_id = %s",(mail,cusid))
			db.commit()
		return render_template('personalinfo.html',cusid = session['cusid'],error="Updated")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)

@app.route("/password")
def password():
	return render_template("passwordchange.html",cusid=session['cusid'])

@app.route("/passupd", methods=['POST'])
def passupd():
	try:
		oldpassword = request.form["old_password"]
		newpassword = request.form["new_password"]
		cusid = session['cusid']
		cur = db.cursor()
		cur.execute("SELECT password FROM Customer WHERE cus_id = %s" %cusid)
		db.commit()
		passkey = cur.fetchone()[0]
		if passkey == oldpassword :
			cur.execute("UPDATE Customer SET password = %s WHERE cus_id = %s",(newpassword,cusid))
			db.commit()
			return render_template('personalinfo.html',cusid = session['cusid'],error="Updated")
		else:
			return render_template('personalinfo.html',cusid=session['cusid'],error="Password didnot Match")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)


@app.route("/active_comp")
def active_comp():
	try:
		cur = db.cursor()
		print 1
		cur.execute("SELECT complaint_no, launch_date, current_state FROM Complaint WHERE cus_id = %s" % session.get("cusid"))
		print 2
		comp_li = cur.fetchall()
		print 3
		print comp_li
		print 4
		db.commit()
		return render_template("activecomplaint.html",cusid=session['cusid'],active_comp_li = comp_li)
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)


@app.route("/activecomplained")
def active_complained():
	if session.get("cusid"):
		return render_template("complaints.html",cusid=session['cusid'])
	else:
		return redirect("/login")

@app.route("/comp")
def comp():
	try:
		return render_template("complaints.html",cusid=session['cusid'])
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'], error = e)

@app.route("/launch_comp")
def launch_comp():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		return render_template("launchcomplaint.html",cusid=session['cusid'],app_exist = appl_li)
	except Exception as e:
		return render_template('index.html',cusid=session['cusid'], error = e)


@app.route("/complained", methods=['POST'])
def complained():
	try:
		cur = db.cursor()
		new_comp_li = request.form.getlist("comp_li[]")
		new_comp_li = [int(i) for i in new_comp_li]
		ini_comp_desc_li = request.form.getlist("comp_desc_li[]")
		ini_comp_desc_li[:] = [item for item in ini_comp_desc_li if item != ""]
		comp_desc_li = {int(new_comp_li[i]):ini_comp_desc_li[i] for i in range(len(new_comp_li))}
		# cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		# prev_comp_li = cur.fetchall()
		# print "ORIGINAL"
		# print prev_comp_li
		cur.execute("INSERT INTO Complaint(cus_id,launch_date,current_state) VALUES (%s,CURDATE(),%s)",(session.get("cusid"), 'active'))
		compid = cur.lastrowid
		print compid
		for i in comp_desc_li.keys():
			cur.execute("INSERT INTO ComplaintDetail(complaint_no,appliance_id,description)VALUES(%s,%s,%s)",(compid,i,comp_desc_li[i]))
		db.commit()
		return render_template('complaints.html',cusid = session['cusid'],error = "Complaint Launched")
	except Exception as e:
		print e
		return render_template('index.html',cusid=session['cusid'],error=e)

@app.route("/about")
def about():
	return render_template("aboutus.html",cusid=session['cusid'])

@app.route("/contact")
def contact():
	return render_template("contactus.html",cusid=session['cusid'])


if __name__ == '__main__':
	app.run(debug=True)