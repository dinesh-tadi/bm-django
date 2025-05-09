import os
from flask import Flask, redirect, render_template, request, sessions, url_for,session
import linecache
import pandas as pd
import csv
import math
from datetime import date
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from random import *
import datetime
import pytz


app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='MySQL@d1075'#
app.config['MYSQL_HOST']='127.0.0.1'#
app.config['MYSQL_DB']='bank'#

app.secret_key="@342$62455asdw"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='g17miniproject@gmail.com'
app.config['MAIL_PASSWORD']='Myminiprojectpswd17'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mysql=MySQL(app)
mail=Mail(app)

otpl=[]
i=int(0)
def otpnum():
    otp=randint(000000,999999)
    otpl.append(otp)
    global i
    i+=1
    return otp

def data(): 
    date = datetime.datetime.now(tz=pytz.UTC)
    dates = str(date.date())
    return dates


def times(): 
    date = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'))
    timer = str(date.time())[:8]
    return timer


interest = {
     "gold" : "10%",
     "personal" : "18%",
     "education" : "6%",
     "FD" : "3%"
}


admin_login_id='admin@iiti.ac.in'
admin_login_pswd='adminpswd'

# @app.route('/')
# def dashboard():
#     return render_template('login.html')

# @app.route('/login.html')
# def logindash():
#     return render_template('login.html')

@app.route('/empdetails.html', methods=['POST', 'GET'])
def emp_details():
        curs=mysql.connection.cursor()
        curs.execute(f"select IFSC,name,Salary,phone_no,email,Address from employee_details where status = 'act';")
        tr = curs.fetchall()
        curs.close()
        return render_template("empdetails.html", t = tr)

# @app.route('/dash.html')
# def dash():
#     curs=mysql.connection.cursor()
#     n = int(session["cid"][3:])
#     curs.execute(f"select Name from customer_details where Cust_ID = {n};")
#     user_name = curs.fetchone()
#     curs.execute(f"select Account_no,account_type,nominee,creation_date from account_details where Cust_ID = {n};")
#     acc = curs.fetchall()
#     acc = list(acc)
#     ap = []
#     for a in acc:
#         a = list(a)
#         if not a[2]:
#             a[2] = "None"
#         q = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[1],a[2],a[3]]
#         ap.append(q)
#     loan = []
#     for a in acc:
#         curs.execute(f"select Loan_Id, Loan_amount,EMI,last_paid from loan_active where account_no = {a[0]};")
#         p = curs.fetchall()
#         for s in p:
#             loan.append(s)
    
#     return render_template('dash.html',username=user_name[0],acc = ap ,l = loan, inte = interest)    

@app.route('/balance.html') 
def balance():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('balance.html' , acc = ac)

@app.route('/cardlimit.html') #changed
def cardlimit():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('cardlimit.html', acc = ac)

@app.route('/casher.html')
def casher():
    return render_template('casher.html')

@app.route('/changepassword.html')
def changepassword():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('changepassword.html', acc = ac)

@app.route('/cheque.html')
def cheque():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('cheque.html', acc =ac)

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/FD.html')
def FD():
    return render_template('FD.html')

@app.route('/feedback.html')
def feedback():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('feedback.html', acc = ac)

@app.route('/loanappl.html')
def loanappl():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('loanappl.html', acc = ac)

# @app.route('/newacc.html')
# def newacc():
#     return render_template('newacc.html')

@app.route('/nominee.html')
def nominee():
    return render_template('nominee.html')

# @app.route('/register.html')
# def register():
#     return render_template('register.html')

@app.route('/trans.html')
def trans():
    n = int(session["cid"][3:])
    curs=mysql.connection.cursor()
    curs.execute(f"select Account_no from account_details where Cust_ID = {n};")
    accounts = curs.fetchall()
    ac = []
    for a in accounts:
        p = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:],a[0]]
        ac.append(p)
    return render_template('trans.html', acc = ac)

@app.route('/addemployee.html')
def addemployee():
    return render_template('addemployee.html')

@app.route('/cashierdash.html')
def cashierdash():
    curs=mysql.connection.cursor()
    n = int(session["cid"][3:])
    curs.execute(f"select Name from employee_details where Employee_ID = {n};")
    user_name = curs.fetchone()
    return render_template('cashierdash.html',username=user_name[0])

@app.route('/cashierprivacy.html')
def cashierprivacy():
    return render_template('cashierprivacy.html')

@app.route('/cashierpswd.html')
def cashierpswd():
    return render_template('cashierpswd.html')

@app.route('/chprivacy.html')
def chprivacy():
    return render_template('chprivacy.html')

@app.route('/chpswd.html')
def chpswd():
    return render_template('chpswd.html')

@app.route('/winaddacc.html')
def winaddacc():
    return render_template('winaddacc.html')

@app.route('/WINaddnominee.html')
def WINaddnominee():
    return render_template('WINaddnominee.html')

@app.route('/WINapploan.html')
def WINapploan():
    return render_template('WINapploan.html')

@app.route('/windash.html')
def windash():
    return render_template('windash.html')

@app.route('/WINreqcredit.html')
def WINreqcredit():
    return render_template('WINreqcredit.html')

@app.route('/WINtransaction.html')
def WINtransaction():
    return render_template('WINtransaction.html')

@app.route('/dashadmin.html')
def dashadmin():
    curs=mysql.connection.cursor()
    n = int(session["cid"][3:])
    curs.execute(f"select Name from employee_details where Employee_ID = {n};")
    user_name = curs.fetchone()
    curs=mysql.connection.cursor()
    curs.execute(f"select SUM(Bank_balance) from account_details;")
    totalsum=curs.fetchone()
    curs=mysql.connection.cursor()
    curs.execute(f"select SUM(Amount_remain) from loan_active;")
    totalloan=curs.fetchone()
    return render_template('dashadmin.html',username=user_name[0],totalsum=totalsum[0],totalloan=totalloan[0],interest=interest)

@app.route('/editemploy.html')
def editemploy():
    curs=mysql.connection.cursor()
    curs.execute(f"select employee_id,title,name,IFSC,phone_no,address,email,salary,date_of_birth from employee_details where status = 'act'")
    emp = curs.fetchall()
    curs.close()
    lis = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6  = []
    i = 0
    for l in emp:
        id = l[1] + "%04d" %l[0]
        d = {'id':id, 'text':id, 'num':i}
        i = i+1
        lis.append(d)
        l1.append(l[2])
        l2.append(l[3])
        l3.append(l[4])
        l4.append(l[5])
        l5.append(l[6])
        l6.append(l[7])
    return render_template('editemploy.html', emp = lis, l1 = l1,l2 = l2,l3=l3,l4=l4,l5=l5,l6=l6)

@app.route('/intrestrates.html')
def intrestrates():
    return render_template('intrestrates.html',interest=interest)

@app.route('/rmvemp.html')
def rmvemp():
    curs=mysql.connection.cursor()
    curs.execute(f"select employee_id,title from employee_details where status = 'act'")
    emp = curs.fetchall()
    lis = []
    for l in emp:
        id = l[1] + "%04d" %l[0]
        print(id)
        lis.append(id)
    curs.close()
    return render_template('rmvemp.html', emp = lis)

# @app.route('/registering', methods=['POST', 'GET'])
# def registering():
#     if request.method == 'GET':
#         return 'Login via login page'
#     if request.method == 'POST':
#         username=request.form['username']
#         email_id=request.form['email_id']
#         phone=request.form['phone_number']
#         address_info=request.form['address_info']
#         DOB=request.form['DOB']
#         PAN=request.form['PAN']
#         emergency_number=request.form['emergency_number']
#         occupation=request.form['occupation']
#         income=request.form['income']
#         Pswd=request.form['password']
#         Pswd_verif=request.form['password_verif']
#         if Pswd_verif==Pswd:
#             curs=mysql.connection.cursor()
#             curs.execute("SELECT PAN FROM customer_details WHERE PAN='%s'"%(PAN))
#             dbrecords = curs.fetchone()
#             if dbrecords!=None:
#                 error="Account already exists"
#                 mysql.connection.commit()
#                 curs.close()
#                 return render_template('registeruseridalreadyexists.html')
#             curs.close()
#             curs=mysql.connection.cursor()
#             mysql.connection.commit()
#             curs.close()
#             msg=Message(subject="Confirmational email", sender="g17miniproject@gmail.com", recipients=[email_id])
#             msg.html=("<h1>OTP</h1>%s"%(str(otpnum())))
#             mail.send(msg)
#             return render_template('html02.html',username=username,email_id=email_id,phone=phone,address_info=address_info,PAN=PAN,Pswd=Pswd,DOB=DOB,emergency_number=emergency_number,occupation=occupation,income=income)  



# @app.route('/otpconfirm', methods=['POST', 'GET'])
# def otpconfirm():
#     if request.method == 'POST':
#         entered_otp=request.form['otp']
#         if otpl[i-1]==int(entered_otp):
#             username=request.form['username']
#             email_id=request.form['email_id']
#             phone=request.form['phone']
#             address_info=request.form['address_info']
#             DOB=request.form['DOB']
#             PAN=request.form['PAN']
#             emergency_number=request.form['emergency_number']
#             occupation=request.form['occupation']
#             income=request.form['income']
#             if not income:
#                 income=0
#             Pswd=request.form['Pswd']
#             curs=mysql.connection.cursor()
#             curs.execute(f"insert into customer_details(IFSC_CODE,Name,Phone_no,Address,Email,Password,PAN,Date_of_birth,Occupation,Emergency_contact,Income) values('IBKN2000010','{username}','{phone}','{address_info}','{email_id}','{Pswd}','{PAN}','{DOB}','{occupation}','{emergency_number}','{income}')")
#             mysql.connection.commit()
#             curs.close()
#             return render_template('login.html')
#         else:
#             return render_template('html04.html')

# @app.route('/loginpage', methods=['POST', 'GET'])
# def login():
#     error=None
#     if request.method == 'POST':
#         User_ID=request.form['user_id']
#         Pswd=request.form['password']
#         if User_ID==admin_login_id and Pswd==admin_login_pswd:
#             return render_template('adminpagefinal.html')

#         curs=mysql.connection.cursor()
#         curs.execute("SELECT userid FROM tb WHERE userid='%s'"%(User_ID))
#         dbrecords = curs.fetchone()
#         if dbrecords==None:
#             error="invalid userid"
#             return render_template('loginpage.html',bool1=False,bool2=True)
#         curs.close()
#         curs=mysql.connection.cursor()
#         curs.execute("SELECT password FROM tb WHERE userid='%s'"%(User_ID))
#         dbpswd = curs.fetchone()
#         curs.close()
#         if Pswd==dbpswd[0]:
#             return render_template('faculty.html') 
#         else:
#             error = "invalid password"
#             return render_template('loginpage.html',bool1=True,bool2=False)
        
# @app.route('/getbalance', methods=['POST', 'GET'])
# def getbalance():
#     if request.method == 'POST':
#         account_number=request.form['account_number']
#         password =request.form['password']
#         curs=mysql.connection.cursor()
#         curs.execute(f"select password from account_details where account_no = {account_number};")
#         pass1 = curs.fetchone()
#         curs.close()
#         if pass1[0] == password:
#             curs=mysql.connection.cursor()
#             curs.execute(f"select bank_balance from account_details where account_no = {account_number};")
#             bal = curs.fetchone()
#             curs.close()
#             return render_template("seebalance.html", bal = bal[0])
#         else:
#             return redirect(url_for('balance'))
        

# @app.route('/getstatement', methods=['POST', 'GET'])
# def getstatement():
#     if request.method == 'POST':
#         account_number=request.form['account_number']
#         password =request.form['password']
#         curs=mysql.connection.cursor()
#         curs.execute(f"select password from account_details where account_no = {account_number};")
#         pass1 = curs.fetchone()
#         curs.close()
#         if pass1[0] == password:
#             curs=mysql.connection.cursor()
#             curs.execute(f"select * from transactions_data where account_no = {account_number};")
#             tr = curs.fetchall()
#             curs.close()
#             return render_template("statement.html", t = tr)
#         else:
#             return redirect(url_for('balance'))

# @app.route('/card_limit', methods=['POST', 'GET'])
# def card_limit():
#     if request.method == 'POST':
#         account_number=request.form['account_number']
#         password=request.form['password']
#         newlimit=request.form['newlimit']
#         curs=mysql.connection.cursor()
#         curs.execute(f"SELECT Password from account_details where Account_no = {int(account_number)};")
#         psw=curs.fetchone()[0]
#         if not password==psw:
#             return render_template('cardlimit.html',msg="please recheck your old password and enter correct password")
#         curs.execute(f"UPDATE credit_card_details SET Max_limit = {int(newlimit)} WHERE Account_no ={int(account_number)};")
#         curs.execute(f"UPDATE credit_card_details SET Daily_limit = {int(newlimit)} WHERE Account_no ={int(account_number)};")
#         curs.execute(f"UPDATE credit_card_details SET Weekly_limit ={7*int(newlimit)} WHERE Account_no ={int(account_number)};")
#         mysql.connection.commit()
#         curs.close()
#         return render_template('success.html')

# @app.route('/applycreditcard', methods=['POST', 'GET'])
# def applycreditcard():
#     if request.method == 'POST':
#         a=request.form['account_number']
#         holder_name=request.form['holder_name']
#         address=request.form['address']
#         phone_number=request.form['phone_number']
#         t = date.today()
#         date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
#         curs=mysql.connection.cursor()
#         curs.execute(f"SELECT IFSC_CODE FROM customer_details where cust_id = (SELECT cust_id from account_details where account_no = {a});")
#         s = curs.fetchone()
#         ifsc = s[0]
#         curs.execute(f"INSERT INTO application(Account_no, IFSC, date_applied, time_applied, applied_for, address) VALUES('{a}','{ifsc}','{date1}','{times()}','CreditCard','{address}');")
#         curs.connection.commit()
#         return render_template('success.html')

@app.route('/applychequebook', methods=['POST', 'GET'])
def applychequebook():
    if request.method == 'POST':
        a=request.form['account_number']
        holder_name=request.form['holder_name']
        address=request.form['address']
        phone_number=request.form['phone_number']
        t = date.today()
        date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
        curs=mysql.connection.cursor()
        curs.execute(f"SELECT IFSC_CODE FROM customer_details where cust_id = (SELECT cust_id from account_details where account_no = {a});")
        s = curs.fetchone()
        ifsc = s[0]
        curs.execute(f"INSERT INTO application(Account_no, IFSC, date_applied, time_applied, applied_for, address) VALUES('{a}','{ifsc}','{date1}','{times()}','chequebook','{address}');")
        curs.connection.commit()
        return render_template('success.html')

@app.route('/fixed_deposit', methods=['POST', 'GET'])
def fixed_deposit():
    if request.method == 'POST':
        account_number=request.form['account_number']
        holder_name=request.form['holder_name']
        amount=request.form['amount']
        duration=request.form['duration']
        curs=mysql.connection.cursor()
        curs.execute("")
        dbrecords = curs.fetchall()
        curs.close()
        dbrecords = list(set(dbrecords))
        return render_template('success.html')

@app.route('/cust_feedback', methods=['POST', 'GET'])
def cust_feedback():
    if request.method == 'POST':
        acc = request.form['acc']
        comment=request.form['comment']
        t = date.today()
        date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
        curs=mysql.connection.cursor()
        curs.execute(f"SELECT IFSC_CODE FROM customer_details where cust_id = (SELECT cust_id from account_details where account_no = {acc});")
        s = curs.fetchone()
        ifsc = s[0]
        curs.close()
        curs=mysql.connection.cursor()
        curs.execute(f"INSERT INTO FEEDBACK(account_no, IFSC, date_applied,time_applied,concern) Values('{acc}', '{ifsc}','{date1}', '{times()}', '{comment}');")
        curs.connection.commit()
        curs.close()
        return render_template('success.html')

# @app.route('/applyloan', methods=['POST', 'GET']) 
# def applyloan():
#     if request.method == 'POST':
#         account_number=request.form['account_number']
#         loan_type=request.form['loan_type']
#         amount = request.form['amount']
#         documents=request.files['documents']
#         t = date.today()
#         date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
#         curs=mysql.connection.cursor()
#         curs.execute(f"SELECT IFSC_CODE FROM customer_details where cust_id = (SELECT cust_id from account_details where account_no = {account_number})")
#         s = curs.fetchone()
#         ifsc = s[0]
#         curs.execute(f"INSERT INTO LOAN_APPLY(Account_No, IFSC, Loan_amount, Loan_type,Loan_intrest,date_applied) Values('{account_number}','{ifsc}','{amount}','{loan_type}','{interest[loan_type]}','{date1}')")
#         mysql.connection.commit()
#         curs.execute(f"Select app_id from loan_apply where app_id = (SELECT MAX(app_id) from loan_apply)")
#         aid = str(curs.fetchall()[0][0])
#         curs.close()
#         app.config["UPLOADSHERE"]=r"static\loan_documents_uploaded"#
#         documents.save(os.path.join(app.config["UPLOADSHERE"], "lapp" + aid +".pdf"))
#         return render_template('success.html')


# @app.route('/loanstatus', methods=['POST', 'GET'])
# def loanstatus():
#     n = int(session["cid"][3:])
#     curs=mysql.connection.cursor()
#     curs.execute(f"select Account_no from account_details where cust_id = {n};")
#     tr = curs.fetchall()
#     loan = []
#     l1 = []
#     l2 = []
#     for a in tr:
#         curs.execute(f"select Loan_Id, Loan_amount, amount_remain,EMI,loan_intrest,last_paid from loan_active where account_no = {a[0]};")
#         p = curs.fetchall()
#         curs.execute(f"select app_id, loan_amount, loan_type, loan_intrest, date_applied from loan_apply where account_no = {a[0]}")
#         q = curs.fetchall()
#         curs.execute(f"select app_id, loan_amount, loan_type, loan_intrest, date_applied,reason from loan_denied where account_no = {a[0]}")
#         r = curs.fetchall()
#         for d in q:
#             d = list(d)
#             d.append("NA")
#             d.append("Pending")
#             l2.append(d)
#         for d in r:
#             d = list(d)
#             print(d)
#             d.append("Denied")
#             l2.append(d)
#         for s in p:
#             l1.append(s)
#     loan.append(l1)
#     loan.append(l2)
#     curs.close()
#     return render_template('loan_status.html', l = loan)

# @app.route('/logindata', methods=['POST', 'GET'])
# def logindata():
#     if request.method == 'POST':
#         user_id=request.form['user_id']
#         password=request.form['password']
#         curs=mysql.connection.cursor()
#         rol = user_id[0:3].upper()
#         n = int(user_id[3:])
#         if rol == "CUS":
#             curs.execute(f"select Password from customer_details where Cust_ID = {n};")
#             pas = curs.fetchone()
#             if not pas:
#                 return render_template("login.html", bpass = False, bacc = True, bfree = False)
#             elif pas[0] == password:
#                 session["cid"]= user_id
#                 return redirect("dash.html")
#             return render_template("login.html", bpass = True, bacc = False, bfree = False)
#         else:
#             curs.execute(f"select Password, title,status,Name from employee_details where Employee_ID = {n};")
#             pas = curs.fetchone()
#             if not pas or pas[1] != rol:
#                 return render_template("login.html", bpass = False, bacc = True, bfree = False)
#             elif pas[2] != "act":
#                 return render_template("login.html", bpass = False, bacc = False, bfree = True)
#             elif pas[0] == password:
#                 session["cid"]= user_id
#                 if rol == "CAS":
#                     return redirect("cashierdash.html")
#                 elif rol == "BAN": 
#                     curs=mysql.connection.cursor()
#                     curs.execute(f"SELECT IFSC FROM employee_details where employee_id = '{int(session['cid'][3:])}'")
#                     s = curs.fetchone()
#                     ifsc = s[0]
#                     curs.execute(f"SELECT APP_ID,ACCOUNT_NO,LOAN_AMOUNT,LOAN_TYPE,LOAN_INTREST,DATE_APPLIED from loan_apply WHERE IFSC ='{ifsc}'")
#                     loans = curs.fetchall()
#                     curs.close()
#                     return render_template("banker.html", name = pas[3], l = loans)
#                 elif rol == "TRN":
#                     curs=mysql.connection.cursor()
#                     curs.execute(f"SELECT IFSC FROM employee_details where employee_id = '{int(session['cid'][3:])}'")
#                     s = curs.fetchone()
#                     ifsc = s[0]
#                     curs.execute(f"SELECT * from trans_appl")
#                     apply = curs.fetchall()
#                     curs.close()
#                     return render_template("transaction_reveiwer.html", name = pas[3], l = apply)
#                 elif rol == "APR":
#                     curs=mysql.connection.cursor()
#                     curs.execute(f"SELECT IFSC FROM employee_details where employee_id = '{int(session['cid'][3:])}'")
#                     s = curs.fetchone()
#                     ifsc = s[0]
#                     curs.execute(f"SELECT APP_ID,ACCOUNT_NO,LOAN_AMOUNT,LOAN_TYPE,LOAN_INTREST,DATE_APPLIED from loan_apply WHERE IFSC ='{ifsc}'")
#                     loans = curs.fetchall()
#                     curs.close()
#                     return "Apllication Reveiwers Page"
#                 elif rol == "WIN":
#                     curs=mysql.connection.cursor()
#                     curs.execute(f"SELECT IFSC FROM employee_details where employee_id = '{int(session['cid'][3:])}'")
#                     s = curs.fetchone()
#                     ifsc = s[0]
#                     curs.execute(f"SELECT FEED_ID,ACCOUNT_NO,DATE_APPLIED,time_applied,concern from feedback WHERE IFSC ='{ifsc}'")
#                     feedbacks = curs.fetchall()
#                     curs.close()
#                     return render_template("cust_executive.html", name = pas[3], f = feedbacks) #change
#                 elif rol == "ADM":
#                     return redirect("dashadmin.html")
#             return render_template("login.html", bpass = True, bacc = False, bfree = False)


# @app.route('/logout', methods=['POST', 'GET'])
# def logout():
#     session.pop("cid",None)
#     return redirect(url_for("logindash"))

@app.route('/empdetails.html', methods=['POST', 'GET'])
def empdetails():
        curs=mysql.connection.cursor()
        curs.execute(f"select IFSC,name,Salary,phone_no,email,Address from employee_details where status = 'act';")
        tr = curs.fetchall()
        curs.close()
        return render_template("empdetails.html", t = tr)

# @app.route('/newaccount', methods=['POST', 'GET'])
# def newaccount():
#     if request.method == 'POST':
#         user_name=request.form['user_name']
#         nominee_name=request.form['nominee_name']
#         phone_number=request.form['phone_number']
#         password=request.form['password']
#         acctype=request.form['acctype']
#         user_photo=request.files['user_photo']
#         n=int(session["cid"][3:])
#         app.config["UPLOADSHERE"]=r"account_profile_photos"
#         user_photo.save(os.path.join(app.config["UPLOADSHERE"], user_photo.filename))
#         curs=mysql.connection.cursor()
#         curs.execute(f"INSERT INTO account_details(password, bank_balance, account_type,creation_date,cust_id,nominee,Branch_address) VALUES('{password}', '0', '{acctype}','{data()}','{n}','{nominee_name}','Indore');")
#         dbrecords = curs.fetchall()
#         curs.connection.commit()
#         curs.close()
#         return render_template('success.html')

@app.route('/changenominee', methods=['POST', 'GET'])
def changenominee():
    if request.method == 'POST':
        account_number=request.form['account_number']
        holder_name=request.form['holder_name']
        new_nominee=request.form['new_nominee']
        curs=mysql.connection.cursor()
        curs.execute("")
        dbrecords = curs.fetchall()
        curs.close()
        dbrecords = list(set(dbrecords))
        return render_template('success.html')

@app.route('/transac', methods=['POST', 'GET'])
def transac():
    if request.method == 'POST':
        facc=request.form['from_account_number']
        tacc=request.form['to_account_number']
        amount=float(request.form['amount'])
        password=request.form['password']
        c=request.form['whichbank']
        curs=mysql.connection.cursor()
        curs.execute(f"select password from account_details where account_no = {facc}")
        pass1 = curs.fetchone()[0]
        print(type(pass1),type(password))
        curs.close()
        if pass1 == password:
            t = date.today()
            date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
            if c == "1":
                curs=mysql.connection.cursor()
                curs.execute(f"select bank_balance from account_details where account_no = {tacc}")
                bal_rec = curs.fetchall()
                curs.execute(f"select bank_balance from account_details where account_no = {facc}")
                bal_sen = curs.fetchone()[0]
                curs.close()
                if amount > bal_sen:
                    msg = "Insufficient Funds!"
                    return render_template('msg.html', msg = msg) 
                if not bal_rec:
                    return render_template("msg.html", msg = "The account does not exist in our Bank Please Recheck!")
                bal_rec = bal_rec[0][0]
                sum1 = bal_rec + bal_sen
                bal1 = bal_sen - amount
                bal2 = bal_rec + amount
                curs=mysql.connection.cursor()
                curs.execute("START TRANSACTION;")
                curs.execute(f"Update account_details set bank_balance = {bal1} where account_no = {facc};")
                curs.execute(f"Update account_details set bank_balance = {bal2} where account_no = {tacc};")
                curs.execute(f"select bank_balance from account_details where account_no = {tacc}")
                brec = curs.fetchone()[0]
                curs.execute(f"select bank_balance from account_details where account_no = {facc}")
                bsen = curs.fetchone()[0]
                print(bsen, brec)
                if sum1 == bsen + brec:
                    status = "success"
                    curs.execute("COMMIT;")
                else:
                    status = "fail"
                    curs.execute("ROLLBACK;")
                curs.connection.commit()
                
                curs.execute(f"INSERT INTO transactions_data(account_no, account_no_to, Date_of_transaction, time_trans, trans_amount, trans_type, done_by) VALUES('{facc}', '{tacc}', '{date1}', '18:03:20', {amount} ,'{status}', 'self');")
                curs.connection.commit()
                curs.close()
                if status == "success":
                    return render_template("success.html")
                else:
                    msg = "Sorry Due to some technical glitch transaction failed, if money debited from yur account it will be refunded"
                    return render_template("msg.html", msg = msg)

            elif c == "2":
                curs=mysql.connection.cursor()
                curs.execute(f"INSERT INTO trans_appl(Account_no, Account_to,amount, date_applied, time_applied) Values('{facc}', '{tacc}', {amount}, '{date1}', '{times()}')")
                curs.connection.commit()
                curs.close()
                msg = "Success! Your transaction will be processed in less than 2hr"
                return render_template("msg.html", msg = msg) 
        else:
            msg = "Wrong Password!"
            return render_template("msg.html", msg = msg)

@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():
    if request.method == 'POST':
        employee_name=request.form['employee_name']
        branch_name=request.form['branch_name']
        title = request.form['role']
        IFSC=request.form['IFSC']
        DOB=request.form['DOB']
        DOJ=request.form['date_of_join']
        phone=request.form['phone_number']
        address=request.form['address']
        email_id=request.form['email_id']
        salary=request.form['salary']
        curs=mysql.connection.cursor()
        date1 = str(date.today())
        curs.execute(f'''INSERT INTO employee_details(name,Title, Branch_address, IFSC, password, date_of_birth, phone_no, Address, email, Salary, date_joined) VALUES('{employee_name}','{title}',"{branch_name}","{IFSC}","{phone}","{DOB}","{phone}","{address}",'{email_id}',{float(salary)}, '{DOJ}');''')
        mysql.connection.commit()
        curs.close()
        return render_template('success.html')

@app.route('/cashier_dash', methods=['POST', 'GET'])
def cashier_dash():
    if request.method == 'POST':
        accoun_number=request.form['account_number']
        account_number=int(accoun_number)
        amount=request.form['amount']
        amount=int(amount)
        type_of_transac=request.form['type_of_transac']
        password=request.form['password']
        curs=mysql.connection.cursor()
        n=int(session["cid"][3:])
        curs.execute(f"select password from employee_details where employee_id = {n}")
        pass1 = curs.fetchone()[0]
        curs.close()
        if pass1 == password:
            if type_of_transac=='deposit':
                curs=mysql.connection.cursor()
                curs.execute(f"UPDATE account_details SET Bank_balance=Bank_balance+{amount} WHERE account_no = {account_number}")
                mysql.connection.commit()
                curs.close()
                return render_template('success.html')
            if type_of_transac=='withdrawl':
                curs=mysql.connection.cursor()
                curs.execute(f"SELECT Bank_balance FROM account_details WHERE account_no = {account_number}")
                dbrecords = curs.fetchall()
                bal=dbrecords[0]
                if bal[0]>= amount:
                    curs.execute(f"UPDATE account_details SET Bank_balance=Bank_balance-{amount} WHERE account_no = {account_number}")
                    mysql.connection.commit()
                    status = "success"
                    curs.execute(f"SELECT Email FROM customer_details WHERE cust_id = (SELECT cust_id FROM account_details WHERE account_no = {account_number} )")
                    dbrecords = curs.fetchall()
                    email_id=dbrecords[0]
                    msg=Message(subject="Confirmational email", sender="g17miniproject@gmail.com", recipients=[email_id[0]])
                    msg.html=("<h1>Transaction review</h1><h6>Amount of %s was withdrawn from your account</h6> <h4>Was this not you? Then please contact out bank</h4>"%amount)
                    mail.send(msg)
                    return render_template("success.html")
                else:
                    status = "fail"
                    curs.execute("ROLLBACK;")
                    msg = "Transaction failed"
                    return render_template("msg.html", msg = msg)
                curs.connection.commit()
                curs.close()
                return status
        else:
            return redirect('cashierdash.html')

@app.route('/cashier_privacy', methods=['POST', 'GET'])
def cashier_privacy():
    if request.method == 'POST':
        cashier_id=request.form['cashier_id']
        old_password=request.form['old_password']
        new_password=request.form['new_password']
        curs=mysql.connection.cursor()
        curs.execute("")
        dbrecords = curs.fetchall()
        curs.close()
        dbrecords = list(set(dbrecords))
        return render_template('success.html')

@app.route('/cashier_pswd', methods=['POST', 'GET'])
def cashier_pswd():
    if request.method == 'POST':
        employee_id=request.form['employee_id']
        oldpassword=request.form['oldpassword']
        newpassword=request.form['newpassword']
        curs=mysql.connection.cursor()
        eid = int(session["cid"][3:])
        curs.execute(f"select password from employee_details where employee_id = {eid};")
        psw=curs.fetchone()[0]
        if not int(employee_id[3:]) == eid:
            return render_template('cashierpswd.html',msg="the employee id is incorrect check again")
        if not oldpassword==psw:
            return render_template('cashierpswd.html', msg="the password you have  entered is incorrect")
        curs.execute(f"UPDATE employee_details SET password='{newpassword}' WHERE employee_id={eid};")
        mysql.connection.commit()
        curs.close()
        return render_template('success.html')

@app.route('/ch_privacy', methods=['POST', 'GET'])
def ch_privacy():
    if request.method == 'POST':
        admin_id=request.form['admin_id']
        old_password=request.form['old_password']
        new_password=request.form['new_password']
        curs=mysql.connection.cursor()
        curs.execute("")
        dbrecords = curs.fetchall()
        curs.close()
        dbrecords = list(set(dbrecords))
        return render_template('success.html')

@app.route('/ch_pswd', methods=['POST', 'GET'])
def ch_pswd():
    if request.method == 'POST':
        employee_id=request.form['employee_id']
        oldpassword=request.form['oldpassword']
        newpassword=request.form['newpassword']
        curs=mysql.connection.cursor()
        eid = int(session["cid"][3:])
        curs.execute(f"select password from employee_details where employee_id = {eid};")
        psw=curs.fetchone()[0]
        if not int(employee_id[3:]) == eid:
            return render_template('chpswd.html',msg="you have entered incorrect employee id")
        if not oldpassword==psw:
            return render_template('chpswd.html', msg="you have entered incorrect password")
        curs.execute(f"UPDATE employee_details SET password='{newpassword}' WHERE employee_id={eid};")
        mysql.connection.commit()
        curs.close()
        return render_template('success.html')

# @app.route('/changepassword', methods=['POST', 'GET'])###
# def change_password():
#     if request.method == 'POST':
#         account_number=request.form['account_number']
#         oldpassword=request.form['oldpassword']
#         newpassword=request.form['newpassword']
#         curs=mysql.connection.cursor()
#         n = int(session["cid"][3:])
#         curs.execute(f"select Account_no from account_details where cust_id = {n};")
#         acc=int(curs.fetchone()[0])
#         curs.execute(f"select Password from account_details where cust_id = {n};")
#         psw=curs.fetchone()[0]
#         if not int(account_number) == acc:
#             return render_template('changepassword.html', msg="the account number you have entered is incorrect")
#         if not oldpassword==psw:
#             return render_template('changepassword.html',msg="please recheck your old password and enter correct password")
#         curs.execute(f"UPDATE account_details SET Password='{newpassword}' WHERE Account_no={acc};")
#         mysql.connection.commit()
#         curs.close()
#         return render_template('success.html')

@app.route('/dashadminsalaries', methods=['POST', 'GET'])
def dashadminsalaries():
    if request.method == 'POST':
        IFSC=request.form['IFSC']
        curs=mysql.connection.cursor()
        curs.execute("")
        dbrecords = curs.fetchall()
        curs.close()
        dbrecords = list(set(dbrecords))
        return render_template('success.html')

@app.route('/edit_employee', methods=['POST', 'GET'])
def edit_employee():
    if request.method == 'POST':
        employee_id=request.form['employee_id']
        employee_name=request.form['employee_name']
        IFSC=request.form['IFSC']
        phone_number=request.form['phone_number']
        address=request.form['address']
        email_id=request.form['email_id']
        salary=request.form['salary']
        emp = int(employee_id[3:])
        curs=mysql.connection.cursor()
        curs.execute(f"UPDATE EMPLOYEE_DETAILS SET name ='{employee_name}',IFSC ='{IFSC}',phone_no = '{phone_number}',address='{address}', email='{email_id}',salary ={salary} WHERE employee_id={emp} ;")
        curs.connection.commit()
        curs.close()
        return render_template('success.html')

@app.route('/interest_rates', methods=['POST', 'GET'])
def interest_rates():
    if request.method == 'POST':
        gold_interest_rate=request.form['gold_interest_rate']
        edu_interest_rate=request.form['edu_interest_rate']
        personal_loan_interest_rate=request.form['personal_loan_interest_rate']
        FD_interest_rate=request.form['FD_interest_rate']
        interest['education']=edu_interest_rate
        interest['FD']=FD_interest_rate
        interest['gold']=gold_interest_rate
        interest['personal']=personal_loan_interest_rate
        return render_template('success.html')

@app.route('/rmv_emp', methods=['POST', 'GET'])
def rmv_emp():
    if request.method == 'POST':
        empl=request.form['employee_user_id']
        admin_privacy_key=request.form['admin_privacy_key']
        curs=mysql.connection.cursor()
        eid = int(session["cid"][3:])
        curs.execute(f"select password from employee_details where employee_id = {eid};")
        psw=curs.fetchone()[0]
        if admin_privacy_key == psw:
            emp = int(empl[3:])
            curs=mysql.connection.cursor()
            curs.execute(f"UPDATE employee_details set status = 'freeze' where employee_id = {emp}")
            curs.connection.commit()
            curs.close()
            return render_template('success.html')
        return render_template("msg.html", msg = "FAILURE")

@app.route('/money', methods=['POST', 'GET'])
def money():
    if request.method == 'POST':
        facc=request.form['account_number']
        tacc=request.form['to_account_number']
        amount=float(request.form['amount'])
        password=request.form['password']
        c=request.form['whichbank']
        curs=mysql.connection.cursor()
        curs.execute(f"select password from employee_details where employee_id = {int(session['cid'][3:])}")
        pass1 = curs.fetchone()[0]
        curs.close()
        if pass1 == password:
            t = date.today()
            date1 = str(t.day) +"/"+ str(t.month)+"/" + str(t.year)
            if c == "1":
                curs=mysql.connection.cursor()
                curs.execute(f"select bank_balance from account_details where account_no = {tacc}")
                bal_rec = curs.fetchall()
                curs.execute(f"select bank_balance from account_details where account_no = {facc}")
                bal_sen = curs.fetchone()[0]
                curs.close()
                if amount > bal_sen:
                    return render_template("msg.html", msg = "Insufficient Funds! Client Does not have enough money in account")
                if not bal_rec:
                    return render_template("msg.html", msg = "The Recievers account does not exist in our Bank! Please Recheck or use other bank option")
                bal_rec = bal_rec[0][0]
                sum1 = bal_rec + bal_sen
                bal1 = bal_sen - amount
                bal2 = bal_rec + amount
                curs=mysql.connection.cursor()
                curs.execute("START TRANSACTION;")
                curs.execute(f"Update account_details set bank_balance = {bal1} where account_no = {facc};")
                curs.execute(f"Update account_details set bank_balance = {bal2} where account_no = {tacc};")
                curs.execute(f"select bank_balance from account_details where account_no = {tacc}")
                brec = curs.fetchone()[0]
                curs.execute(f"select bank_balance from account_details where account_no = {facc}")
                bsen = curs.fetchone()[0]
                print(bsen, brec)
                if sum1 == bsen + brec:
                    status = "success"
                    curs.execute("COMMIT;")
                else:
                    status = "fail"
                    curs.execute("ROLLBACK;")
                curs.connection.commit()
                curs.execute(f"INSERT INTO transactions_data(account_no, account_no_to, Date_of_transaction, time_trans, trans_amount, trans_type, done_by) VALUES('{facc}', '{tacc}', '{date1}', '{times()}', {amount} ,'{status}', '{session['cid']}');")
                curs.connection.commit()
                curs.close()
                if status == "success":
                    return render_template("success.html")
                else:
                    return render_template("msg.html", msg = "Sorry Due to some technical glitch transaction failed, if money debited from yur account it will be refunded, kindly retry!")

            elif c == "2":
                curs=mysql.connection.cursor()
                curs.execute(f"INSERT INTO trans_appl(Account_no, Account_to,amount, date_applied, time_applied) Values('{facc}', '{tacc}', {amount}, '{date1}', '{times()}')")
                curs.connection.commit()
                curs.close()
                return render_template("msg.html", msg = "Success! Your transaction will be processed in less than 2hr" ) 
        else:
            return render_template("msg.html", msg = "Wrong Password!")

@app.route('/review/<id>', methods=['POST', 'GET'])
def review(id): 
    curs = mysql.connection.cursor()
    curs.execute(f"SELECT APP_ID,ACCOUNT_NO,LOAN_AMOUNT,LOAN_TYPE,LOAN_INTREST,DATE_APPLIED from loan_apply WHERE app_id ='{id}'")
    loans = curs.fetchall()
    curs.close()
    return render_template('review.html', l = loans)

@app.route('/reviewed', methods=['POST', 'GET']) 
def reviewed():
    if request.method == "POST":
        lid = request.form['lid']
        d = request.form['accept']
        if d == "yes":
            curs = mysql.connection.cursor()
            curs.execute(f"SELECT * FROM loan_apply where app_id = '{lid}'")
            p = curs.fetchone()
            curs.execute(f"SELECT MAX(LOAN_ID) FROM LOAN_ACTIVE")
            linti = curs.fetchone()[0]
            curs.execute("START TRANSACTION;")
            curs.execute(f"DELETE from loan_apply where app_id='{lid}'")
            curs.execute(f"INSERT INTO LOAN_ACTIVE(Account_no,loan_amount,loan_type,loan_intrest,date_granted,amount_remain) Values('{p[1]}','{p[3]}','{p[4]}','{p[5]}','{data()}','{p[3]}');")
            curs.execute(f"SELECT EXISTS(SELECT * FROM LOAN_apply where APP_ID = {lid})")
            y = curs.fetchone()[0]
            curs.execute(f"SELECT MAX(LOAN_ID) FROM LOAN_ACTIVE")
            lfinal = curs.fetchone()[0]
            if lfinal == linti or y == 1:
                curs.execute("ROLLBACK;")
            else:
                curs.execute("COMMIT;")
            curs.connection.commit()
            curs.close()
        elif d == "no":
            r = request.form['reason']
            curs = mysql.connection.cursor()
            curs.execute(f"SELECT * FROM loan_apply where app_id = '{lid}'")
            p = curs.fetchone()
            curs.execute("START TRANSACTION;")
            curs.execute(f"DELETE from loan_apply where app_id='{lid}'")
            curs.execute(f"INSERT INTO LOAN_Denied(App_ID,Account_no,loan_amount,loan_type,loan_intrest,date_applied,date_denied,reason) Values('{p[0]}','{p[1]}','{p[3]}','{p[4]}','{p[5]}','{p[6]}','{data()}','{r}');")
            curs.execute(f"SELECT EXISTS(SELECT * FROM LOAN_apply where APP_ID = {lid})")
            y = curs.fetchone()[0]
            curs.execute(f"SELECT EXISTS(SELECT * FROM LOAN_DENIED where APP_ID = {lid})")
            bcon = curs.fetchone()[0]
            if bcon == 0 or y == 1:
                curs.execute("ROLLBACK;")
            else:
                curs.execute("COMMIT")
            curs.connection.commit()
            curs.close()
    return render_template('success.html')

@app.route('/proceed/<id>', methods=['POST', 'GET'])
def proceed(id):
    curs = mysql.connection.cursor()
    curs.execute(f"SELECT * from trans_appl where app_id = {id};")
    p = curs.fetchone()
    curs.execute(f"SELECT MAX(TRANS_ID) FROM transactions_data")
    i = curs.fetchone()[0]
    s = session["cid"]
    curs.execute("START TRANSACTION")
    curs.execute(f"DELETE from trans_appl where app_id='{id}'")
    curs.execute(f"INSERT INTO transactions_data(Account_no,Account_no_to,date_of_transaction,time_trans,trans_amount,trans_type,done_by) Values('{p[1]}','{p[2]}','{p[4]}','{p[5]}','{p[3]}','success', '{s}');")
    curs.execute(f"SELECT MAX(TRANS_ID) FROM transactions_data")
    f = curs.fetchone()[0]
    curs.execute(f"SELECT EXISTS(SELECT * FROM trans_appl where APP_ID = {id})")
    y = curs.fetchone()[0]
    if i == f or y == 1:
        curs.execute("ROLLBACK")
    else:
        curs.execute("COMMIT")
    curs.connection.commit()
    curs.close()
    return render_template("success.html")

@app.route('/reply/<id>', methods=['POST', 'GET'])
def reply(id): 
    curs = mysql.connection.cursor()
    curs.execute(f"SELECT Feed_id,ACCOUNT_NO,DATE_APPLIED,Time_applied,concern from feedback WHERE feed_id ='{id}'")
    feed = curs.fetchall()
    curs.close()
    return render_template('reply.html', f = feed)


@app.route('/replied', methods=['POST', 'GET']) 
def replied():
    if request.method == "POST":
        fid = request.form['lid']
        res = request.form['reply']
        curs = mysql.connection.cursor()
        curs.execute(f"SELECT * FROM feedback where feed_id = '{fid}'")
        p = curs.fetchone()
        # curs.execute(f"SELECT MAX(feed_ID) FROM feed_solved")
        # linti = curs.fetchone()[0]
        curs.execute("START TRANSACTION;")
        curs.execute(f"DELETE from feedback where feed_id='{fid}'")
        curs.execute(f"INSERT INTO feed_solved Values('{p[0]}','{p[1]}','{p[2]}','{p[3]}','{p[4]}','{data()}','{times()}','{p[5]}','emp','{res}');")
        curs.execute(f"SELECT EXISTS(SELECT * FROM feedback where feed_ID = {fid})")
        y = curs.fetchone()[0]
        curs.execute(f"SELECT EXISTS(SELECT * FROM feed_solved where feed_ID = {fid})")
        x = curs.fetchone()[0]
        if y == 1 or x ==0:
            curs.execute("ROLLBACK;")
        else:
            curs.execute(f"SELECT Email FROM customer_details WHERE cust_id = (SELECT cust_id FROM account_details WHERE account_no = '{p[1]}' )")
            dbrecords = curs.fetchall()
            email_id=dbrecords[0]
            print(email_id[0])
            curs.execute("COMMIT;")
            msg=Message(subject="Reply From Bank", sender="g17miniproject@gmail.com", recipients=[email_id[0]])
            msg.html=(f"<h1>Glad to Serve You!</h1><h4>Dear Customer</h4><h6>{res}</h6> <h4>This is the reply to your feedback: </h4><h6>{p[5]}</h6>")
            mail.send(msg)
        curs.connection.commit()
        curs.close()
    return render_template('success.html')
if __name__ =="__main__":
    app.run(debug=True)