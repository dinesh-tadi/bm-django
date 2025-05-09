from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import random
import os
from datetime import date, datetime
from django.http import HttpResponse
import json

interest = {
    "gold": "10%",
    "personal": "18%",
    "education": "6%",
    "FD": "3%"
}

def landing(request):
    """Landing/login page"""
    if "cid" in request.session:
        return redirect('dashboard')
    return render(request, 'login.html')

def test_db(request):
    try:
        with connection.cursor() as c:
            c.execute('SELECT * FROM "customerTable" LIMIT 1')
            row = c.fetchone()
        return HttpResponse(f"Row: {row}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def getcustomerid(emailid):
    with connection.cursor() as curs:
        try:
            # Get user name
            curs.execute('SELECT "customerID" FROM "customerTable" WHERE "emailid" = %s;', [emailid])
            customerID = curs.fetchone()
        except Exception as e:
            print(f"Database error: {e}")
            customerID = 401
    return customerID

def getemployeeid(emailid):
    with connection.cursor() as curs:
        try:
            # Get user name
            curs.execute('SELECT "employeeID" FROM "employeeTable" WHERE "emailid" = %s;', [emailid])
            employeeID = curs.fetchone()
        except Exception as e:
            print(f"Database error: {e}")
            employeeID = 401
    return employeeID

def dashboard(request):
    """Dashboard view after login"""
    if "cid" not in request.session:
        return redirect('landing')
    userid = request.session["cid"]
    emailid = userid[4:]
    
    with connection.cursor() as curs:
        try:
            # Get user name
            curs.execute('SELECT "name", "customerID" FROM "customerTable" WHERE "emailid" = %s;', [emailid])
            user_name, customerID = curs.fetchone()
            # print(user_name)
            
            # Get account details
            curs.execute('SELECT "accountNo", "accountType", "nominee", "createdAt" FROM "accountTable" WHERE "customerID" = %s;', [customerID])
            acc = curs.fetchall()
            ap = []
            # print(acc[0][0])
            for a in list(acc):
                a = list(a)
                if not a[2]:
                    a[2] = "None"
                q = [str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[1], a[2], a[3]]
                ap.append(q)
                
            # Get loan details
            loan = []
            for a in acc:
                curs.execute('SELECT "loanID", "amount", "EMIamount", "lastEMI" FROM "loanGrantedTable" WHERE "accountNo" = %s;', [a[0]])
                p = curs.fetchall()
                for s in p:
                    loan.append(s)

        except Exception as e:
            print(f"Database error: {e}")  # For development debugging
            user_name = ["Test User"]  # Fallback data
            ap = [["123xxxx789", "Savings", "None", "2024-01-01"]]  # Fallback data
            loan = []

    
                
    context = {
        'username': user_name if user_name else "Test User",
        'acc': ap,
        'l': loan,
        'inte': interest
    }
    
    return render(request, 'dash.html', context)

# Add all the required view functions
def transfer(request):
    return render(request, 'trans.html')

def balance(request):
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    with connection.cursor() as curs:
        curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [getcustomerid(emailid)])
        accounts = curs.fetchall()
    ac = [[str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[0]] for a in accounts]
    return render(request, 'balance.html', {'acc': ac})

def new_account(request):
    return render(request, 'newacc.html')

def loan_status(request):
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    
    with connection.cursor() as curs:
        # Get customer ID
        customerID = getcustomerid(emailid)
        
        # Get account numbers
        curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [customerID])
        accounts = curs.fetchall()
        
        active_loans = []
        pending_loans = []
        
        for account in accounts:
            # Get active loans
            curs.execute("""
                SELECT "loanID", "amount", "amountRemaining", "EMIamount", "interest", "lastEMI" 
                FROM "loanGrantedTable" 
                WHERE "accountNo" = %s
            """, [account[0]])
            active_loans.extend(curs.fetchall())
            
            # Get pending applications
            curs.execute("""
                SELECT "applicationID", "amount", "appliedfor", "interest", "createdAt" 
                FROM "applicationTable" 
                WHERE "accountNo" = %s AND "status" = 'pending'
            """, [account[0]])
            pending = list(curs.fetchall())
            for p in pending:
                p = list(p)
                p.extend(["NA", "Pending"])
                pending_loans.append(p)
            
            # Get denied applications
            curs.execute("""
                SELECT "applicationID", "amount", "appliedfor", "interest", "createdAt", "reason" 
                FROM "applicationTable" 
                WHERE "accountNo" = %s AND "status" = 'denied'
            """, [account[0]])
            denied = list(curs.fetchall())
            for d in denied:
                d = list(d)
                d.append("Denied")
                pending_loans.append(d)
    
    context = {
        'active_loans': active_loans,
        'pending_loans': pending_loans
    }
    return render(request, 'loan_status.html', context)

def change_password(request):
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    customerID = getcustomerid(emailid)

    
    if request.method == 'GET':
        with connection.cursor() as curs:
            curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [getcustomerid(emailid)])
            accounts=curs.fetchall()
            ac = [[str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[0]] for a in accounts]
            return render(request, 'changepassword.html', {'acc': ac})

    if request.method == 'POST':
        account_number = request.POST['account_number']
        oldpassword = request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        
        with connection.cursor() as curs:
            # Get customer ID and account number
            customerID = getcustomerid(emailid)
            curs.execute('SELECT "accountNo", "password" FROM "accountTable" WHERE "customerID" = %s', [customerID])
            account = curs.fetchone()
            
            if not account:
                return render(request, 'changepassword.html', {'msg': "Account not found", 'acc': []})
            
            acc_no, current_password = account
            
            if str(account_number) != str(acc_no):
                return render(request, 'changepassword.html', {'msg': "The account number you have entered is incorrect", 'acc': []})
            
            if oldpassword != current_password:
                return render(request, 'changepassword.html', {'msg': "Please recheck your old password and enter correct password", 'acc': []})
            
            # Update password
            curs.execute('UPDATE "accountTable" SET "password" = %s WHERE "accountNo" = %s', [newpassword, acc_no])
            
        return render(request, 'success.html')
    
    return redirect('dashboard')

def card_limit(request):
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    with connection.cursor() as curs:
        curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [getcustomerid(emailid)])
        accounts = curs.fetchall()
    ac = [[str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[0]] for a in accounts]
    return render(request, 'cardlimit.html', {'acc': ac})

def loan_apply(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        loan_type = request.POST['loan_type']
        amount = request.POST['amount']
        duration = request.POST['duration']
        documents = request.FILES['documents']
        
        with connection.cursor() as curs:
            # Get IFSC code
            curs.execute('SELECT "IFSC_code" FROM "customerTable" WHERE "customerID" = (SELECT "customerID" FROM "accountTable" WHERE "accountNo" = %s)', [account_number])
            s = curs.fetchone()
            ifsc = s[0] if s else None
            
            # Insert loan application
            curs.execute("""
                INSERT INTO "loanRequestTable" 
                ("accountNo", "IFSC_code", "amount", "loanType", "interest", "createdAt", "duration" ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [account_number, ifsc, amount, loan_type, int(interest.get(loan_type, '0')[:-1])/100, datetime.now(), duration])
            
            # Get the application ID
            aid = curs.lastrowid
        
        # Save document
        doc_path = os.path.join(settings.MEDIA_ROOT, 'loan_documents_uploaded')
        os.makedirs(doc_path, exist_ok=True)
        with open(os.path.join(doc_path, f"lapp_{aid}.pdf"), 'wb+') as destination:
            for chunk in documents.chunks():
                destination.write(chunk)
                
        return render(request, 'success.html')
    
    # GET request - display form
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    with connection.cursor() as curs:
        curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [getcustomerid(emailid)])
        accounts = curs.fetchall()
    ac = [[str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[0]] for a in accounts]
    return render(request, 'applyloan.html', {'acc': ac})

def feedback(request):
    return render(request, 'feedback.html')

def contact(request):
    return render(request, 'contact.html')

def logout(request):
    # Add logout logic here
    del request.session['cid']
    return redirect('landing')

def register(request):
    """Display registration form"""
    return render(request, 'register.html')

def register_submit(request):
    """Handle registration form submission"""
    if request.method == 'POST':
        username = request.POST['username']
        email_id = request.POST['email_id']
        phone = request.POST['phone_number']
        address_info = request.POST['address_info']
        DOB = request.POST['DOB']
        PAN = request.POST['PAN']
        emergency_number = request.POST['emergency_number']
        occupation = request.POST['occupation']
        income = request.POST['income']
        password = request.POST['password']
        password_verif = request.POST['password_verif']

        if password != password_verif:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        with connection.cursor() as curs:
            curs.execute('SELECT "PAN" FROM "customerTable" WHERE "PAN"=%s', [PAN])
            if curs.fetchone():
                return render(request, 'registeruseridalreadyexists.html')

        # Generate OTP
        otp = random.randint(100000, 999999)
        request.session['registration_otp'] = otp
        request.session['registration_data'] = {
            'username': username,
            'email_id': email_id,
            'phone': phone,
            'address_info': address_info,
            'DOB': DOB,
            'PAN': PAN,
            'emergency_number': emergency_number,
            'occupation': occupation,
            'income': income,
            'password': password,
        }

        # Send OTP email
        send_mail(
            'Registration OTP and login details',
            f'Your OTP is: {otp} \n After confirming the OTP, you will be redirected to the login page \n Please use the username: CUS_{email_id} and password: {password[0:3]}xxxx to login',
            settings.DEFAULT_FROM_EMAIL,
            [email_id],
            fail_silently=False,
        )

        return render(request, 'otpconfirmation.html', request.session['registration_data'])

    return redirect('register')

def otp_confirm(request):
    """Handle OTP confirmation"""
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('registration_otp')
        registration_data = request.session.get('registration_data')

        if not stored_otp or not registration_data:
            return redirect('register')

        if int(entered_otp) == stored_otp:
            with connection.cursor() as curs:
                curs.execute("""
                    INSERT INTO "customerTable"
                    ("IFSC_code", "name", "createdAt", "mobile", "address", "emailid", "password", "PAN", 
                    "dob", "occupation", "emergencyContact", "income")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    'IBKN2000010',
                    registration_data['username'],
                    datetime.now(),
                    registration_data['phone'],
                    registration_data['address_info'],
                    registration_data['email_id'],
                    registration_data['password'],
                    registration_data['PAN'],
                    registration_data['DOB'],
                    registration_data['occupation'],
                    registration_data['emergency_number'],
                    registration_data['income'] or 0,
                ])

            # Clear session data
            del request.session['registration_otp']
            del request.session['registration_data']

            return redirect('login')
        else:
            return render(request, 'wrongotp.html')

    return redirect('register')

def create_account(request):
    """Handle new account creation"""
    if "cid" not in request.session:
        return redirect('landing')
    userid = request.session["cid"]
    emailid = userid[4:]
    
    with connection.cursor() as curs:
        try:
            # Get user name
            curs.execute('SELECT "customerID" FROM "customerTable" WHERE "emailid" = %s;', [emailid])
            customerID = curs.fetchone()
        except Exception as e:
            print(f"Database error: {e}")
            customerID = 401

    if request.method == 'POST':
        user_name = request.POST['user_name']
        nominee_name = request.POST['nominee_name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        acctype = request.POST['acctype']
        user_photo = request.FILES['user_photo']

        # Save photo
        photo_path = os.path.join(settings.MEDIA_ROOT, 'account_profile_photos')
        os.makedirs(photo_path, exist_ok=True)
        with open(os.path.join(photo_path, user_photo.name), 'wb+') as destination:
            for chunk in user_photo.chunks():
                destination.write(chunk)

        # Get customer ID from session
        # customerID = int(request.session.get("cid", "0")[3:])
        
        with connection.cursor() as curs:
            curs.execute("""
                INSERT INTO "accountTable"
                ("password", "amount", "accountType", "createdAt", "customerID", "nominee", "IFSC_code")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [password, 5000000, acctype, datetime.now(), customerID, nominee_name, 'IBKN2000010'])

        return render(request, 'success.html')

    return redirect('new_account')

def logindata(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        rol = user_id[0:3].upper()
        emailid = user_id[4:]

        with connection.cursor() as curs:
            if rol == "CUS":
                print(emailid)
                curs.execute('SELECT "password" FROM "customerTable" WHERE "emailid" = %s', [emailid])
                pas = curs.fetchone()
                if not pas:
                    return render(request, "login.html", {'bpass': False, 'bacc': True, 'bfree': False})
                elif pas[0] == password:
                    request.session["cid"] = user_id
                    return redirect('dashboard')
                return render(request, "login.html", {'bpass': True, 'bacc': False, 'bfree': False})
            else:
                curs.execute('SELECT "password", "role", "status", "name" FROM "employeeTable" WHERE "emailid" = %s', [emailid])
                pas = curs.fetchone()
                # print(pas, rol)
                if not pas or pas[1].upper() != rol:
                    print("login failed")
                    return render(request, "login.html", {'bpass': False, 'bacc': True, 'bfree': False})
                elif pas[2] != "active":
                    print("login failed not active")
                    return render(request, "login.html", {'bpass': False, 'bacc': False, 'bfree': True})
                elif pas[0] == password:
                    print("login successful")
                    request.session["cid"] = user_id
                    if rol == "CAS":
                        return redirect('cashierdash')
                    elif rol == "BAN":
                        curs.execute('SELECT "IFSC_code" FROM "employeeTable" WHERE "emailid" = %s', [emailid])
                        s = curs.fetchone()
                        ifsc = s[0]
                        curs.execute('SELECT "applicationID", "accountNo", "appliedfor", "createdAt" FROM "applicationTable" WHERE "IFSC_code" = %s', [ifsc])
                        loans = curs.fetchall()
                        return render(request, "banker.html", {'name': pas[3], 'l': loans})
                    elif rol == "TRN":
                        curs.execute('SELECT "IFSC_code" FROM "employeeTable" WHERE "emailid" = %s', [emailid])
                        s = curs.fetchone()
                        ifsc = s[0]
                        curs.execute('SELECT * FROM "applicationTable"')
                        apply = curs.fetchall()
                        return render(request, "transaction_reveiwer.html", {'name': pas[3], 'l': apply})
                    elif rol == "APR":
                        curs.execute('SELECT "IFSC_code" FROM "employeeTable" WHERE "emailid" = %s', [emailid])
                        s = curs.fetchone()
                        ifsc = s[0]
                        curs.execute('SELECT "applicationID", "accountNo", "appliedfor", "createdAt" FROM "applicationTable" WHERE "IFSC_code" = %s', [ifsc])
                        loans = curs.fetchall()
                        return render(request, "application_reviewer.html", {'name': pas[3], 'l': loans})
                    elif rol == "WIN":
                        curs.execute('SELECT "IFSC_code" FROM "employeeTable" WHERE "emailid" = %s', [emailid])
                        s = curs.fetchone()
                        ifsc = s[0]
                        curs.execute('SELECT "feedbackID", "customerID", "createdAt", "feedback" FROM "feedbackTable" WHERE "IFSC_code" = %s', [ifsc])
                        feedbacks = curs.fetchall()
                        return render(request, "cust_executive.html", {'name': pas[3], 'f': feedbacks})
                    elif rol == "ADM":
                        print("admin")
                        return redirect('dashadmin')
                return render(request, "login.html", {'bpass': True, 'bacc': False, 'bfree': False})
    return redirect('landing')

def cheque(request):
    if "cid" not in request.session:
        return redirect('landing')
    n = int(request.session["cid"][3:])
    with connection.cursor() as curs:
        curs.execute('SELECT "accountNo" FROM "accountTable" WHERE "customerID" = %s', [n])
        accounts = curs.fetchall()
    ac = [[str(a[0])[0:3] + "xxxx" + str(a[0])[-3:], a[0]] for a in accounts]
    return render(request, 'cheque.html', {'acc': ac})

def getbalance(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')
        with connection.cursor() as curs:
            curs.execute('SELECT "password" FROM "accountTable" WHERE "accountNo" = %s', [account_number])
            pass1 = curs.fetchone()
            if pass1 and pass1[0] == password:
                curs.execute('SELECT "amount" FROM "accountTable" WHERE "accountNo" = %s', [account_number])
                bal = curs.fetchone()
                return render(request, "seebalance.html", {'bal': bal[0] if bal else 0})
        return redirect('balance')
    return redirect('balance')

def getstatement(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')
        with connection.cursor() as curs:
            curs.execute('SELECT "password" FROM "accountTable" WHERE "accountNo" = %s', [account_number])
            pass1 = curs.fetchone()
            if pass1 and pass1[0] == password:
                curs.execute('SELECT "transactionID", "createdAt", "action", "fromAccountNo", "toAccountNo", "amount" FROM "onlineTransactionTable" WHERE "fromAccountNo" = %s OR "toAccountNo" = %s', [account_number, account_number])
                tr = curs.fetchall()
                #reaarange tr to match statement.html
                #tr original order: id createdat(2025-05-08 23:10:19) action(done by) from to amount
                # id:0 from:3 to:4 date:1 time:1 amount:5 done by:2
                #split createdat datetime.datetimeinto date and time and add to tr
                #rans_ID	from	To	Date	Time	Amount	Done by
                tr = [[t[0], str(t[3])[0:3] + "xxxx" + str(t[3])[-3:], str(t[4])[0:3] + "xxxx" + str(t[4])[-3:], t[1].strftime('%d/%m/%Y'), t[1].strftime('%H:%M:%S'), t[5] if str(t[3]) == account_number else -t[5], t[2]] for t in tr]
                return render(request, "statement.html", {'t': tr})
        return redirect('balance')
    return redirect('balance')

def card_limit_post(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')
        newlimit = request.POST.get('newlimit')
        with connection.cursor() as curs:
            curs.execute('SELECT "password" FROM "accountTable" WHERE "accountNo" = %s', [account_number])
            psw = curs.fetchone()
            if not psw or password != psw[0]:
                return render(request, 'cardlimit.html', {'msg': "please recheck your old password and enter correct password"})
            curs.execute('UPDATE "debitCards" SET "maxDailyLimit" = %s, "weeklyLimit" = %s WHERE "Account_no" = %s',
                         [int(newlimit), 7*int(newlimit), account_number])
        return render(request, 'success.html')
    return redirect('card_limit')

def applycreditcard(request):
    if request.method == 'POST':
        a = request.POST.get('account_number')
        holder_name = request.POST.get('holder_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        t = date.today()
        date1 = f"{t.day}/{t.month}/{t.year}"
        with connection.cursor() as curs:
            curs.execute('SELECT "IFSC_code" FROM "customerTable" WHERE "customerID" = (SELECT "customerID" FROM "accountTable" WHERE "accountNo" = %s)', [a])
            s = curs.fetchone()
            ifsc = s[0] if s else None
            curs.execute('INSERT INTO "applicationTable" ("accountNo", "IFSC_code", "createdAt", "appliedfor", "address") VALUES (%s, %s, %s, %s, %s)',
                         [a, ifsc, datetime.now(), 'CreditCard', address])
        return render(request, 'success.html')
    return redirect('dashboard')

def applychequebook(request):
    if request.method == 'POST':
        a = request.POST.get('account_number')
        holder_name = request.POST.get('holder_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        t = date.today()
        date1 = f"{t.day}/{t.month}/{t.year}"
        with connection.cursor() as curs:
            curs.execute('SELECT "IFSC_code" FROM "customerTable" WHERE "customerID" = (SELECT "customerID" FROM "accountTable" WHERE "accountNo" = %s)', [a])
            s = curs.fetchone()
            ifsc = s[0] if s else None
            curs.execute('INSERT INTO "applicationTable" ("accountNo", "IFSC_code", "createdAt", "appliedfor", "address") VALUES (%s, %s, %s, %s, %s)',
                         [a, ifsc, datetime.now(), 'chequebook', address])
        return render(request, 'success.html')
    return redirect('dashboard')

def dashadmin(request):
    if "cid" not in request.session:
        return redirect('landing')
    emailid = request.session["cid"][4:]
    employeeID = getemployeeid(emailid)
    
    with connection.cursor() as curs:
        # Get admin name
        curs.execute('SELECT "name" FROM "employeeTable" WHERE "employeeID" = %s', [employeeID])
        user_name = curs.fetchone()
        
        # Get total bank balance
        curs.execute('SELECT SUM("amount") FROM "accountTable"')
        totalsum = curs.fetchone()
        
        # Get total loan amount
        curs.execute('SELECT SUM("amountRemaining") FROM "loanGrantedTable"')
        totalloan = curs.fetchone()
    
    return render(request, 'dashadmin.html', {
        'username': user_name[0] if user_name else '',
        'totalsum': totalsum[0] if totalsum else 0,
        'totalloan': totalloan[0] if totalloan else 0,
        'interest': interest
    })

def editemploy(request):
    if "cid" not in request.session:
        return redirect('landing')
    
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee_name = request.POST['employee_name']
        IFSC = request.POST['IFSC']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        email_id = request.POST['email_id']
        salary = request.POST['salary']
        emp = int(employee_id[3:])
        
        with connection.cursor() as curs:
            curs.execute("""
                UPDATE "employeeTable" 
                SET "name" = %s, "IFSC_code" = %s, "mobile" = %s, "address" = %s, 
                    "emailid" = %s, "salary" = %s 
                WHERE "employeeID" = %s
            """, [employee_name, IFSC, phone_number, address, email_id, salary, emp])
        
        return render(request, 'success.html')
        
    # GET method: fetch employee details and build lists for the template
    with connection.cursor() as curs:
        curs.execute('SELECT "employeeID", "title", "name", "IFSC_code", "mobile", "address", "emailid", "salary", "dob" FROM "employeeTable" WHERE "status" = %s', ['active'])
        emp_data = curs.fetchall()
    lis = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    for i, l in enumerate(emp_data):
        display = f"{l[2]} - {l[1]}"  # e.g., "John Doe - MAN"
        d = {'id': str(l[0]), 'text': display, 'num': i}  # Convert UUID to string
        lis.append(d)
        l1.append(l[2])  # name
        l2.append(l[3])  # IFSC
        l3.append(l[4])  # phone
        l4.append(l[5])  # address
        l5.append(l[6])  # email
        l6.append(l[7])  # salary
    emp_json = json.dumps(lis)
    return render(request, 'editemploy.html', {'emp': emp_json, 'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4, 'l5': l5, 'l6': l6})

def interestrates(request):
    if "cid" not in request.session:
        return redirect('landing')
    return render(request, 'interestrates.html', {'interest': interest})

def rmv_emp(request):
    if "cid" not in request.session:
        return redirect('landing')
        
    if request.method == 'POST':
        empl = request.POST['employee_user_id']
        admin_privacy_key = request.POST['admin_privacy_key']
        
        with connection.cursor() as curs:
            emailid = request.session["cid"][4:]
            employeeID = getemployeeid(emailid)
            curs.execute('SELECT "password" FROM "employeeTable" WHERE "employeeID" = %s', [employeeID])
            psw = curs.fetchone()
            
            if psw and admin_privacy_key == psw[0]:
                curs.execute('UPDATE "employeeTable" SET "status" = %s WHERE "employeeID" = %s', ['freeze', empl])
                return render(request, 'success.html')
        
        return render(request, "msg.html", {'msg': "FAILURE"})
    
    if request.method == 'GET':
        with connection.cursor() as curs:
            curs.execute('SELECT "name", "employeeID", "title" FROM "employeeTable" WHERE "status" = %s', ['active'])
            emp = curs.fetchall()
            lis = []
            for l in emp:
                lis.append({
                    'id': f"{l[1]}",  # employeeID
                    'text': f"{l[0]} - {l[2]}"  # name - title
                })
    return render(request, 'rmvemp.html', {'emp': lis})

def empdetails(request):
    if "cid" not in request.session:
        return redirect('landing')
        
    with connection.cursor() as curs:
        curs.execute('''
            SELECT "IFSC_code", "name", "salary", "mobile", "emailid", "address" 
            FROM "employeeTable" 
            WHERE "status" = 'active'
        ''')
        tr = curs.fetchall()
    
    return render(request, "empdetails.html", {'t': tr})

def add_employee(request):
    if "cid" not in request.session:
        return redirect('landing')
        
    if request.method == 'POST':
        employee_name = request.POST['employee_name']
        role = request.POST['role']
        DOB = request.POST['DOB']
        DOJ = request.POST['date_of_join']
        phone = request.POST['phone_number']
        address = request.POST['address']
        email_id = request.POST['email_id']
        salary = request.POST['salary']
        title = request.POST['Title']
        
        with connection.cursor() as curs:
            curs.execute("""
                INSERT INTO "employeeTable" 
                ("name", "role", "title", "IFSC_code", "password", "dob", "mobile", "address", "emailid", "salary", "dateJoined", "status") 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                employee_name, role, title, "IBKN2000010", phone, DOB, phone, 
                address, email_id, int(salary), DOJ, "active"
            ])
        
        return render(request, 'success.html')


    return render(request, 'addemployee.html')

def dashadminsalaries(request):
    if "cid" not in request.session:
        return redirect('landing')
        
    if request.method == 'POST':
        IFSC = request.POST['IFSC']
        with connection.cursor() as curs:
            curs.execute('SELECT * FROM "employeeTable" WHERE "IFSC_code" = %s', [IFSC])
            dbrecords = list(set(curs.fetchall()))
        return render(request, 'success.html')
    
    return redirect('dashadmin')

def edit_employee(request):
    if "cid" not in request.session:
        return redirect('landing')
    
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee_name = request.POST['employee_name']
        IFSC = request.POST['IFSC']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        email_id = request.POST['email_id']
        salary = request.POST['salary']
        
        with connection.cursor() as curs:
            curs.execute("""
                UPDATE "employeeTable" 
                SET "name" = %s, "IFSC_code" = %s, "mobile" = %s, "address" = %s, 
                    "emailid" = %s, "salary" = %s 
                WHERE "employeeID" = %s
            """, [employee_name, IFSC, phone_number, address, email_id, salary, employee_id])
        
        return render(request, 'success.html')
    
    # GET method: fetch employee details and build lists for the template
    with connection.cursor() as curs:
        curs.execute('SELECT "employeeID", "title", "name", "IFSC_code", "mobile", "address", "emailid", "salary", "dob" FROM "employeeTable" WHERE "status" = %s', ['active'])
        emp_data = curs.fetchall()
    lis = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    print(emp_data)
    for i, l in enumerate(emp_data):
        display = f"{l[2]} - {l[1]}"  # e.g., "John Doe - MAN"
        d = {'id': str(l[0]), 'text': display, 'num': i}  # Convert UUID to string
        lis.append(d)
        l1.append(l[2])  # name
        l2.append(l[3])  # IFSC
        l3.append(l[4])  # phone
        l4.append(l[5])  # address
        l5.append(l[6])  # email
        l6.append(l[7])  # salary
    print(lis)
    emp_json = json.dumps(lis)
    print(emp_json)
    return render(request, 'editemploy.html', {'emp': emp_json, 'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4, 'l5': l5, 'l6': l6})

def interest_rates(request):
    if "cid" not in request.session:
        return redirect('landing')
        
    if request.method == 'POST':
        global interest
        interest['education'] = request.POST['edu_interest_rate']
        interest['FD'] = request.POST['FD_interest_rate']
        interest['gold'] = request.POST['gold_interest_rate']
        interest['personal'] = request.POST['personal_loan_interest_rate']
        return render(request, 'success.html')
    
    return render(request, 'interestrates.html', {'interest': interest})

# Add other view functions as needed... 