from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # This will be the login page
    path('test-db/', views.test_db),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer, name='transfer'),
    path('balance/', views.balance, name='balance'),
    path('new-account/', views.new_account, name='new_account'),
    path('new-account/create/', views.create_account, name='create_account'),  # POST endpoint for new account
    path('loan-status/', views.loan_status, name='loan_status'),
    path('change-password/', views.change_password, name='change_password'),
    path('card-limit/', views.card_limit, name='card_limit'),
    path('loan-apply/', views.loan_apply, name='loan_apply'),
    path('feedback/', views.feedback, name='feedback'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    # Registration related URLs
    path('register/', views.register, name='register'),
    path('register/submit/', views.register_submit, name='register_submit'),
    path('register/otp/', views.otp_confirm, name='otp_confirm'),
    # Login related URLs
    path('login/', views.landing, name='login'),
    path('logindata/', views.logindata, name='logindata'),
    path('login/submit/', views.dashboard, name='login_submit'),
    path('getbalance/', views.getbalance, name='getbalance'),
    path('getstatement/', views.getstatement, name='getstatement'),
    path('card_limit/', views.card_limit_post, name='card_limit_post'),
    path('applycreditcard/', views.applycreditcard, name='applycreditcard'),
    path('applychequebook/', views.applychequebook, name='applychequebook'),
    # Admin dashboard and related URLs
    path('dashadmin/', views.dashadmin, name='dashadmin'),
    path('editemploy/', views.editemploy, name='editemploy'),
    path('interestrates/', views.interestrates, name='interestrates'),
    path('empdetails/', views.empdetails, name='empdetails'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('dashadminsalaries/', views.dashadminsalaries, name='dashadminsalaries'),
    path('edit_employee/', views.edit_employee, name='edit_employee'),
    path('interest_rates/', views.interest_rates, name='interest_rates'),
    path('rmv_emp/', views.rmv_emp, name='rmv_emp'),
    path('proceed/<str:id>/', views.proceed_transaction, name='proceed_transaction'),
    path('reply_view/<str:id>/', views.reply_view, name='reply_view'),
    path('replied_view/', views.replied_view, name='replied_view'),
    # Customer Executive URLs
    path('cust-executive/', views.cust_executive, name='cust_executive'),
    # Loan Review URLs
    path('review/<str:id>/', views.review_loan, name='review_loan'),
    path('process-review/', views.process_review, name='process_review'),
    # Banker URLs
    path('banker/', views.banker, name='banker'),
] 