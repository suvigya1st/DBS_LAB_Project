from flask import Flask,render_template,session,request,jsonify,json,redirect,url_for
from hashlib import md5
import MySQLdb
import requests

app = Flask(__name__)
app.secret_key = "aw456787uioSHUI4w5eQuighepuihqetoghRUIGHQEOh"

db = MySQLdb.connect("localhost","root","password","hsh2" )



# def connectNode():
# 	s.connect((nodemcuHost,nodemcuPort))

@app.route("/")
@app.route("/homepage")
def homepage():
	return render_template("homePage.html")


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
		cur.execute("INSERT INTO Customer(password,cus_name_id,cus_email_id,addr_id) VALUES (%s,%s,%s,%s)",(password,nameid,mail,addrid))
		db.commit()
		cusid = cur.lastrowid
		cur.execute("INSERT INTO Customer_contact VALUES (%s,%s)",(cusid,cont))
		db.commit()
		return render_template('login.html',cusid = cusid)
	else:
		return redirect("/reg")

@app.route("/registerEmp")
def registerEmp():
	return render_template('registerEmp.html')

@app.route("/regEmp",methods=['GET','POST'])
def regEmp():	
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
		compname = request.form["company_name"]
		complocation = request.form["company_location"]
		salary = int(request.form["salary"])
		cur = db.cursor()
		cur.execute("INSERT INTO Name(first_name,middle_name,last_name) VALUES (%s,%s,%s)",(fname,mname,lname))
		db.commit()
		nameid = cur.lastrowid
		cur.execute("INSERT INTO Address(building_name,street_name,city,state) VALUES (%s,%s,%s,%s)",(building,street,city,state))
		db.commit()
		addrid = cur.lastrowid
		cur.execute("INSERT INTO Company(company_name,location) VALUES (%s,%s)",(compname,complocation))
		db.commit()
		cur.execute("INSERT INTO Employee(password,company_name,emp_name_id,emp_email,addr_id,salary) VALUES (%s,%s,%s,%s,%s,%s)",(password,compname,nameid,mail,addrid,salary))
		db.commit()
		empid = cur.lastrowid
		cur.execute("INSERT INTO Employee_contact(emp_id,emp_contact_no) VALUES (%s,%s)",(empid,cont))
		db.commit()
		return render_template('loginEmp.html', empid = empid)


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

@app.route("/loginemp")
def loginemp():
	return render_template("loginEmp.html")

@app.route("/login_test_emp", methods=['POST'])
def login_test_emp():
	userkey = request.form["username"]
	passkey = request.form["password"]
	try:
		error = None
		cur = db.cursor()
		cur.execute("SELECT * FROM Employee WHERE emp_id = %s" %userkey);
		if cur.fetchone():
			cur.execute("SELECT password FROM Employee where emp_id = %s",[userkey]);
			for row in cur.fetchall():	
				if passkey == row[0]:
					session['empid'] = userkey
					return render_template("indexEmp.html",empid = userkey)
				else:
					error = "Wrong Password"
					return render_template('loginEmp.html', error=error)
		else:
			error = "User Not Registered"
			return render_template('loginEmp.html', error=error)
	except Exception as e:
		return render_template("loginEmp.html",error=e)

@app.route("/index")
def index():
	return render_template("index.html",cusid=session['cusid'])

@app.route("/home")
def home():
	return render_template("index.html",cusid=session['cusid'])

@app.route("/homeEmp")
def homeEmp():
	return render_template("indexEmp.html",empid=session['empid'])

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


serverIP = 'http://192.168.43.137/gpio/2/'

@app.route("/controled", methods=['POST'])
def controled():
	global serverIP
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
				requests.get(serverIP+'on')
			elif (i not in new_app_li) and (appl_li[i]=='on'):
				#UPDATE that application current_state to 'off'

				cur.execute("UPDATE Appliance SET current_state = %s WHERE appliance_id = %s" ,('off',i))
				requests.get(serverIP+'off')
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

@app.route("/perinfoEmp")
def perinfoEmp():
	return render_template("personalinfoEmp.html",empid=session['empid'])


@app.route("/view")
def view():
	return render_template("viewinfo.html",cusid=session['cusid'])

@app.route("/viewEmp")
def viewEmp():
	return render_template("viewinfoEmp.html",empid=session['empid'])


@app.route("/updt")
def updt():
	return render_template("updateinfo.html",cusid=session['cusid'])

@app.route("/view_name")
def view_name():
	try:
		cur = db.cursor()
		cur.execute("SELECT cus_name_id FROM Customer WHERE cus_id = %s" %session.get("cusid"))
		db.commit()
		nameid = cur.fetchone()[0]
		cur.execute("SELECT first_name,middle_name,last_name FROM Name WHERE name_id = %s" %nameid)
		db.commit()
		name = cur.fetchall()
		return render_template("view_name.html",cusid=session['cusid'],viewname = name)
	except Exception as e:
		print e
		return render_template('viewinfo.html', error = e)

@app.route("/view_name_emp")
def view_name_emp():
	try:
		cur = db.cursor()
		cur.execute("SELECT emp_name_id FROM Employee WHERE emp_id = %s" %session.get("empid"))
		db.commit()
		nameid = cur.fetchone()[0]
		cur.execute("SELECT first_name,middle_name,last_name FROM Name WHERE name_id = %s" %nameid)
		db.commit()
		name = cur.fetchall()
		return render_template("view_name_emp.html",empid=session['empid'],viewname = name)
	except Exception as e:
		print e
		return render_template('viewinfoEmp.html', error = e)


@app.route("/view_address")
def view_address():
	try:
		cur = db.cursor()
		cur.execute("SELECT addr_id FROM Customer WHERE cus_id = %s" %session.get("cusid"))
		db.commit()
		addrid = cur.fetchone()[0]
		cur.execute("SELECT building_name,street_name,city,state FROM Address WHERE addr_id = %s" %addrid)
		db.commit()
		address = cur.fetchall()
		return render_template("view_address.html",cusid=session['cusid'],viewaddress = address)
	except Exception as e:
		print e
		return render_template('viewinfo.html', error = e)


@app.route("/view_address_emp")
def view_address_emp():
	try:
		cur = db.cursor()
		cur.execute("SELECT addr_id FROM Employee WHERE emp_id = %s" %session.get("empid"))
		db.commit()
		addrid = cur.fetchone()[0]
		cur.execute("SELECT building_name,street_name,city,state FROM Address WHERE addr_id = %s" %addrid)
		db.commit()
		address = cur.fetchall()
		return render_template("view_address_emp.html",empid=session['empid'],viewaddress = address)
	except Exception as e:
		print e
		return render_template('viewinfoEmp.html', error = e)


@app.route("/view_contact")
def view_contact():
	try:
		cur = db.cursor()
		cur.execute("SELECT cus_contact_no FROM Customer_contact WHERE cus_id = %s" %session.get("cusid"))
		db.commit()
		contact = cur.fetchall()
		return render_template("view_contact.html",cusid=session['cusid'],viewcontact = contact)
	except Exception as e:
		print e
		return render_template('viewinfo.html', error = e)


@app.route("/view_contact_emp")
def view_contact_emp():
	try:
		cur = db.cursor()
		cur.execute("SELECT emp_contact_no FROM Employee_contact WHERE emp_id = %s" %session.get("empid"))
		db.commit()
		contact = cur.fetchall()
		return render_template("view_contact_emp.html",empid=session['empid'],viewcontact = contact)
	except Exception as e:
		print e
		return render_template('viewinfoEmp.html', error = e)


@app.route("/view_email")
def view_email():
	try:
		cur = db.cursor()
		cur.execute("SELECT cus_email_id FROM Customer WHERE cus_id = %s" %session.get("cusid"))
		db.commit()
		email = cur.fetchall()
		return render_template("view_email.html",cusid=session['cusid'],viewemail = email)
	except Exception as e:
		print e
		return render_template('viewinfo.html', error = e)


@app.route("/view_email_emp")
def view_email_emp():
	try:
		cur = db.cursor()
		cur.execute("SELECT emp_email FROM Employee WHERE emp_id = %s" %session.get("empid"))
		db.commit()
		email = cur.fetchall()
		return render_template("view_email_emp.html",empid=session['empid'],viewemail = email)
	except Exception as e:
		print e
		return render_template('viewinfoEmp.html', error = e)


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
		if new_comp_li:
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

@app.route("/compemp")
def compemp():
	try:
		cur = db.cursor()
		cur.execute("SELECT complaint_no FROM ComplaintAssigned WHERE emp_id = %s" %session.get("empid"))
		db.commit()
		comp_li = cur.fetchall()
		print comp_li
		return render_template("complaintEmp.html",empid=session['empid'],comp_li = comp_li)
	except Exception as e:
		return render_template('indexEmp.html',empid=session['empid'],error =e)

@app.route("/compdetail", methods=['POST','GET'])
def compdetail():
	try:
		cur = db.cursor()
		comp_no = request.form['radio_selected']
		print comp_no
		if comp_no:
			cur.execute("SELECT cus_id,launch_date,current_state,appliance_id, description FROM Complaint natural join ComplaintDetail WHERE complaint_no = %s"% comp_no)
			comp_det = list(cur.fetchall()[0])
			cus_id = int(comp_det[0])
			comp_det[0] = comp_no
			comp_det = tuple(comp_det)
			print comp_det
			cur.execute("SELECT first_name,middle_name,last_name,cus_email_id,addr_id FROM Customer, Name WHERE cus_id = %s and Customer.cus_name_id = Name.name_id" % cus_id)
			cus_det = list(cur.fetchall())
			cus_det = list(cus_det[0])
			cus_name = cus_det[0]+' '+cus_det[1]+' '+cus_det[2]
			cus_det = cus_det[3:]
			cus_det.insert(0,cus_name)
			cur.execute("SELECT building_name, street_name,city,state FROM Address WHERE addr_id = %s" % cus_det[-1])
			cus_addr_det = list(cur.fetchall()[0])
			cus_addr_det = " ".join(cus_addr_det)
			cus_det[-1] = cus_addr_det
			cus_det = tuple(cus_det)
			print cus_det
			cur.execute("SELECT cus_contact_no FROM Customer_contact WHERE cus_id = %s" % cus_id)
			cus_contacts = tuple(list(cur.fetchall()[0]))
			print cus_contacts
		return render_template('compDetails.html',empid=session['empid'],comp_det = comp_det, cus_det = cus_det, cus_contacts = cus_contacts)
	except Exception as e:
	 	return render_template('indexEmp.html',empid=session['empid'] ,error =e)



@app.route("/resolved", methods=['POST'])
def resolved():
		try:
			cur = db.cursor()
			print 1
			comp_no = request.form['complaint_no']
			print comp_no
			cur.execute("UPDATE Complaint SET current_state = 'inactive' WHERE complaint_no = %s" %(comp_no))			
			db.commit()
			return render_template("indexEmp.html", empid = session['empid'], error = "Complaint resolved")
		except Exception as e:
			return render_template("indexEmp.html",empid=session['empid'] ,error =e)

@app.route("/report")
def report():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		db.commit()
		res=[]
		print 1
		apps = cur.fetchall()
		for i in range(len(apps)):
			print 2
			appid = int(apps[i][0])
			cur.execute("SELECT appliance_id,switch_on_time,switch_off_time,TIMESTAMPDIFF(HOUR,switch_on_time,switch_off_time),TIMESTAMPDIFF(MINUTE,switch_on_time,switch_off_time),TIMESTAMPDIFF(SECOND,switch_on_time,switch_off_time) FROM Activity WHERE appliance_id = %s" % appid)
			db.commit()
			print 3
			rep = list(cur.fetchall()[0])
			hours = rep[-3]
			if(hours):
				minu = rep[-2]-60*hours
				sec = rep[-1]-60*60*hours-60*minu
			else:
				hours=""
				minu=""
				sec=""
			rep = rep[:-2]
			rep[-1]=str(hours)+':'+str(minu)+':'+str(sec)
			rep = tuple(rep)
			res.append(rep)
			print 4
		return render_template('report.html',cusid=session['cusid'] , rep=res)
	except Exception as e:
		return render_template("index.html",cusid=session['cusid'], error = e)


@app.route("/about")
def about():
	return render_template("aboutus.html",cusid=session['cusid'])

@app.route("/contact")
def contact():
	return render_template("contactus.html",cusid=session['cusid'])

@app.route("/aboutEmp")
def aboutEmp():
	return render_template("aboutusEmp.html",empid=session['empid'])

@app.route("/contactEmp")
def contactEmp():
	return render_template("contactusEmp.html",empid=session['empid'])


if __name__ == '__main__':
	app.run(debug=True)