from django.urls import path

# from .views import UserRegistrationView, 
from .views import home, registerpage_view, LogoutView, UserLoginView

# app_name = 'bank'

urlpatterns = [
    path("home/", home, name="home-page"),
    path("register/", registerpage_view, name="register-page"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    # path("register/", UserRegistrationView.as_view(), name="user_registration"),
]
