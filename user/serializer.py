from django.utils.functional import empty
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail

from .models import OTP, Specialization, StudentRegistration, User
from django.db import transaction


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()
        if user and user.is_active and user.check_password(attrs["password"]):
            return user

        raise serializers.ValidationError("Invalid email or password")


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all(), "email already exists.")]
    )
    name = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        password1 = attrs.pop("password1")
        password2 = attrs.pop("password2")
        if password2 != password1:
            raise serializers.ValidationError({"password2": "password did not match"})

        with transaction.atomic():
            print(password1)
            user = User.objects.create_user(**attrs, password=password1)

            # send otp mail
            OTP.send_otp(user)

            return user


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
    image = serializers.ImageField(write_only=True, required=False)
    name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = StudentRegistration
        fields = "__all__"
        read_only_fields = [
            "created_on",
            "last_update",
            "user",
            "application_id",
            "status",
        ]

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        name = validated_data.pop("name", None)
        res = super().create(validated_data)

        user = res.user
        if image:
            user.image = image
        if name:
            user.image = image
        if user or image:
            user.save()

        return res

    def update(self, instance, validated_data):
        # print(validated_data)
        image = validated_data.pop("image", None)
        name = validated_data.pop("name", None)

        res = super().update(instance, validated_data)
        res.status = "pending"
        res.save()

        user = res.user
        if image:
            user.image = image
        if name:
            user.image = image
        if user or image:
            user.save()
        return res


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
