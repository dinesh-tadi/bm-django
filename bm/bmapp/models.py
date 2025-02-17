# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounttable(models.Model):
    accountno = models.BigAutoField(db_column='accountNo', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Customertable', models.DO_NOTHING, db_column='customerID')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    nominee = models.TextField(blank=True, null=True)
    accounttype = models.CharField(db_column='accountType', blank=True, null=True)  # Field name made lowercase.
    ifsc_code = models.TextField(db_column='IFSC_code', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accountTable'
        db_table_comment = 'table for storing accounts'


class Applicationtable(models.Model):
    applicationid = models.BigAutoField(db_column='applicationID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    status = models.CharField(blank=True, null=True)
    accountno = models.ForeignKey(Accounttable, models.DO_NOTHING, db_column='accountNo', blank=True, null=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Customertable', models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.
    appliedfor = models.TextField(blank=True, null=True)
    ifsc_code = models.TextField(db_column='IFSC_code', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'applicationTable'
        db_table_comment = 'table for concern applications'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customertable(models.Model):
    customerid = models.BigAutoField(db_column='customerID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    mobile = models.CharField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    pan = models.TextField(db_column='PAN', unique=True, blank=True, null=True)  # Field name made lowercase.
    occupation = models.TextField(blank=True, null=True)
    emailid = models.TextField(blank=True, null=True)
    emergencycontact = models.CharField(db_column='emergencyContact', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customerTable'
        db_table_comment = 'table to store customer info'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employeetable(models.Model):
    employeeid = models.BigAutoField(db_column='employeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField()
    mobile = models.CharField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    ifsc_code = models.TextField(db_column='IFSC_code', blank=True, null=True)  # Field name made lowercase.
    salary = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    emailid = models.CharField(db_column='emailID', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employeeTable'
        db_table_comment = 'Table storing employee data'


class Feedbacktable(models.Model):
    feedbackid = models.BigAutoField(db_column='feedbackID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    status = models.CharField(blank=True, null=True)
    feedback = models.CharField(blank=True, null=True)
    customerid = models.ForeignKey(Customertable, models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.
    ifsc_code = models.TextField(db_column='IFSC_code', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feedbackTable'
        db_table_comment = 'table for storing feedback'


class Loandeniedtable(models.Model):
    loanid = models.BigAutoField(db_column='loanID', primary_key=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    interest = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    customerid = models.ForeignKey(Customertable, models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loanDeniedTable'
        db_table_comment = 'Table containing info about denied loans'


class Loangrantedtable(models.Model):
    loanid = models.BigAutoField(db_column='loanID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    duration = models.CharField(blank=True, null=True)
    lastemi = models.DateTimeField(db_column='lastEMI', blank=True, null=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customertable, models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.
    emiamount = models.DecimalField(db_column='EMIamount', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loanGrantedTable'
        db_table_comment = 'table to store granted loan details'


class Loanrequesttable(models.Model):
    loadid = models.BigAutoField(db_column='loadID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    interest = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    duration = models.CharField(blank=True, null=True)
    customerid = models.ForeignKey(Customertable, models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.
    ifsc_code = models.TextField(db_column='IFSC_code', blank=True, null=True)  # Field name made lowercase.
    loantype = models.TextField(db_column='loanType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loanRequestTable'
        db_table_comment = 'table for storing loan requests'


class Offlinetransactiontable(models.Model):
    transactionid = models.BigAutoField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    action = models.CharField(blank=True, null=True)
    accountno = models.ForeignKey(Accounttable, models.DO_NOTHING, db_column='accountNo', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    employeeid = models.BigIntegerField(db_column='employeeID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offlineTransactionTable'
        db_table_comment = 'table for on-site transactions'


class Onlinetransactiontable(models.Model):
    transactionid = models.BigAutoField(db_column='transactionID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    action = models.CharField(blank=True, null=True)
    fromaccountno = models.ForeignKey(Accounttable, models.DO_NOTHING, db_column='fromAccountNo', blank=True, null=True)  # Field name made lowercase.
    toaccountno = models.BigIntegerField(db_column='toAccountNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'onlineTransactionTable'
        db_table_comment = 'table to store online transactions'


class Processingtable(models.Model):
    applicationid = models.OneToOneField(Applicationtable, models.DO_NOTHING, db_column='applicationID', primary_key=True)  # Field name made lowercase.
    employeeid = models.ForeignKey(Employeetable, models.DO_NOTHING, db_column='employeeID')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'processingTable'
        db_table_comment = 'table to store applications processed'


class Responsetable(models.Model):
    responseid = models.BigAutoField(db_column='responseID', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    employeeid = models.BigIntegerField(db_column='employeeID', blank=True, null=True)  # Field name made lowercase.
    feedback = models.CharField(blank=True, null=True)
    customerid = models.ForeignKey(Customertable, models.DO_NOTHING, db_column='customerID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'responseTable'
        db_table_comment = 'table for feedback responses'
