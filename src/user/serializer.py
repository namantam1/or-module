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
