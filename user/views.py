from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from user.models import OTP, StudentRegistration, User

from django.core.files.storage import default_storage

from rest_framework.permissions import IsAuthenticated

from user.serializer import (
    StudentRegistrationSerializer,
    UploadFileSerializer,
    VerifyEmailSerializer,
)


def home(request):
    return render(request, "user/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "user/register.html")


@login_required
def dashboard(request):
    if request.user.is_staff:
        return render(request, "user/admin.html")
    else:
        return render(request, "user/dashboard.html")


@api_view(["POST"])
def verify_email(request):
    serializer = VerifyEmailSerializer(data=request.data)
    if serializer.is_valid(True):
        validated_data = serializer.validated_data

        user = User.objects.create(
            email=validated_data.get("email"), name=validated_data.get("name")
        )

        registration = StudentRegistration.objects.create(
            user=user, application_id=validated_data.get("application_id")
        )

        return Response({"registration_id": registration.id}, 201)

    return Response({}, 200)


@api_view(["POST"])
def register_student(request):
    pass


@api_view(["POST"])
def validate_otp(request):
    data = request.data
    email = data.get("email")
    otp = data.get("otp")
    if email and otp:
        res = OTP.validate(otp, email)
        if res is True:
            return Response({}, 201)

    return Response({"attempts_left": res}, 400)


class StudentRegistrationView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentRegistrationSerializer

    def get_object(self):
        pk = self.kwargs.pop("pk")
        return get_object_or_404(
            StudentRegistration.objects.filter(id=pk), user=self.request.user
        )


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
