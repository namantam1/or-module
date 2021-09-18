from django.urls import path
from .views import (
    StudentRegistrationView,
    UploadFileView,
    dashboard,
    home,
    register,
    register_student,
    validate_otp,
    verify_email,
)

urlpatterns = [
    path("login/", home, name="home"),
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("verify_email/", verify_email, name="verify_email"),
    path("validate_otp/", validate_otp, name="validate_otp"),
    path(
        "register_student/<int:pk>/",
        StudentRegistrationView.as_view(),
        name="register_student",
    ),
    path("upload_file/", UploadFileView.as_view(), name="upload_file"),
]
