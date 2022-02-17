from django.urls import path

# from .views import UserRegistrationView, 
from .views import home, registerpage_view, LogoutView, UserLoginView, TransactionView, verify_otp, TransactionReport

# app_name = 'bank'

urlpatterns = [
    path("home/", home, name="home-page"),
    path("register/", registerpage_view, name="register-page"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("transfer/", TransactionView, name="transfer-money"),
    path("verify_otp/", verify_otp, name="verify-otp"),
    path("transaction_report/", TransactionReport, name="transaction-report"),
]
