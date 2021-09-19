from django.urls import path

from .views import (
    LoginView,
    Register,
    SpecializationListView,
    StudentCreateView,
    StudentRegistrationView,
    StudentUpdateView,
    UploadFileView,
    dashboard,
    home,
    logout,
    resend_otp,
    verify_otp,
)

urlpatterns = [
    path("", home, name="home"),
    path("logout/", logout, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("resend_otp/", resend_otp, name="verify_email"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path(
        "student_register/",
        StudentCreateView.as_view(),
        name="student_register",
    ),
    path(
        "student_update/",
        StudentUpdateView.as_view(),
        name="student_update",
    ),
    path("upload_file/", UploadFileView.as_view(), name="upload_file"),
    path(
        "specialization/<str:department>/",
        SpecializationListView.as_view(),
        name="specialization",
    ),
]
