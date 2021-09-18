from django.urls import path
from .views import dashboard, home, register, verify_email

urlpatterns = [
    path("login/", home, name="home"),
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("verify_email/", verify_email, name="verify_email"),
]
