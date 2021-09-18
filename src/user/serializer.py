from django.contrib.auth.decorators import user_passes_test
from django.core.checks import messages
from django.db.models import query
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import StudentRegistration, User


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all(), "email already exists.")]
    )
    name = serializers.CharField()
    application_id = serializers.CharField(
        validators=[
            UniqueValidator(
                StudentRegistration.objects.all(), "application id already exists."
            )
        ]
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "email_verified",
            "name",
            "image",
            "date_joined",
            "is_active",
            "is_staff",
        ]


class StudentRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentRegistration
        fields = "__all__"
        read_only_fields = ["created_on", "last_update", "user", "application_id"]


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
