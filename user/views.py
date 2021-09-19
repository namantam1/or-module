from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from user.models import (
    OTP,
    Category,
    Department,
    Specialization,
    StudentRegistration,
    User,
)
from user.serializer import (
    LoginSerializer,
    RegisterSerializer,
    SpecializationSerializer,
    StudentRegistrationSerializer,
    UploadFileSerializer,
    UserSerializer,
)


def home(request):
    if request.user.is_authenticated:
        return redirect("register")
    return render(request, "index.html")


def logout(request):
    logout_user(request)
    return redirect("login")


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        # redirect to register view to check completion of form
        if request.user.is_authenticated:
            return redirect("register")

        return render(request, "login.html")

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        user = serializer.validated_data
        login_user(request, user)
        return Response({}, 200)


class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        user = request.user
        form = 1

        if user.is_authenticated:
            if user.is_staff or hasattr(user, "studentregistration"):
                return redirect("dashboard")

            elif user.email_verified:
                form = 3

            else:
                form = 2

        data = {
            "departments": Department.objects.all(),
            "categories": Category.objects.all(),
            "form": form,
        }
        return render(request, "register.html", context=data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        user = serializer.validated_data
        login_user(request, user)
        return Response(UserSerializer(user).data, 201)


@login_required
def dashboard(request):
    if request.user.is_staff:
        return render(request, "admin_dashboard.html")
    else:
        student = request.user.studentregistration
        data = {
            "user": request.user,
            "student": student,
            "departments": Department.objects.all(),
            "categories": Category.objects.all(),
            "specializations": Specialization.objects.filter(
                department__value=student.department
            ),
        }

        return render(request, "dashboard.html", context=data)


@api_view(["POST"])
@login_required
def verify_otp(request):
    otp = request.data.get("otp")
    if otp is not None and request.user.validate_otp(otp):
        return Response({}, 200)

    return Response("Invalid otp", 400)


@login_required
@api_view(["POST"])
def resend_otp(request):
    if not request.user.email_verified:
        OTP.send_otp(request.user)
        return Response({}, 200)

    return Response("Something went wrong", 400)


class StudentRegistrationView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudentRegistrationSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status", "")
        return StudentRegistration.objects.filter(status__in=status.split(","))


class StudentUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentRegistrationSerializer

    def get_object(self):
        # print(self.request.data)
        return get_object_or_404(
            StudentRegistration.objects.all(), user=self.request.user
        )


class StudentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer

    def perform_create(self, serializer):
        if not self.request.user.email_verified:
            raise ValidationError({"user": "Email not verified!"}, "permission denied")

        return serializer.save(user=self.request.user)


class SpecializationListView(ListAPIView):
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        department = self.kwargs.pop("department", "")
        return Specialization.objects.filter(department__value=department)


class UploadFileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file = serializer.validated_data.get("file")
            img_res = default_storage.save(f"files/{file.name}", file)
            response = {"file_url": default_storage.url(img_res)}
            return Response(response, status=200)
