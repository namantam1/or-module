from django.shortcuts import render, resolve_url
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import StudentRegistration, User

from user.serializer import VerifyEmailSerializer


def home(request):
    return render(request, "user/login.html")


def register(request):
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

        StudentRegistration.objects.create(
            user=user, application_id=validated_data.get("application_id")
        )

        return Response(serializer.data, 201)

    return Response({}, 200)
