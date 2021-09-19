from datetime import time, timedelta
import random
from django import db
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models.expressions import F
from django.db.models.query_utils import select_related_descend

from django.utils import timezone

import secrets


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Main User model for API
    """

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    image = models.ImageField(upload_to="profile")
    email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return str(self.email or self.id)

    def validate_otp(self, otp):
        if hasattr(self, "otp") and self.otp.validate(otp):
            self.email_verified = True
            self.save()
            return True

        return False


class Department(models.Model):
    value = models.CharField(max_length=30)

    def __str__(self) -> str:
        return str(self.value or self.id)


class Specialization(models.Model):
    value = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.value or self.id)


class Category(models.Model):
    value = models.CharField(max_length=15)

    def __str__(self) -> str:
        return str(self.value or self.id)

    class Meta:
        verbose_name_plural = "Categories"


class StudentRegistration(models.Model):
    GENDER = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    STATUS = [
        ("pending", "pending"),
        ("rejected", "rejected"),
        ("accepted", "accepted"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER, max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, verbose_name="Date of birth", blank=True)
    application_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
    registration_number = models.CharField(
        max_length=30, unique=True, null=True, blank=True
    )
    aadhar = models.CharField(max_length=15, unique=True, null=True, blank=True)
    passport = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    specialization = models.CharField(
        max_length=100, db_index=True, null=True, blank=True
    )
    category = models.CharField(max_length=15, db_index=True, null=True, blank=True)
    pwd = models.BooleanField(default=False)
    documents = models.FileField(
        "URL of document uploaded",
        upload_to="files",
        blank=True,
        null=True,
    )
    notes = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user or self.id)


def get_expire_time():
    return timezone.now() + timedelta(minutes=2)


def get_otp():
    return random.randint(100000, 999999)


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=3)
    expire_on = models.DateTimeField(default=get_expire_time)
    value = models.IntegerField(default=get_otp)

    def __str__(self) -> str:
        return str(self.user or self.id)

    @property
    def is_expired(self):
        if self.expire_on < timezone.now() or self.attempts <= 0:
            self.delete()
            return True
        return False

    def validate(self, otp):
        if not self.is_expired and str(self.value) == str(otp):
            self.delete()
            return True
        if self.id:
            self.attempts = F("attempts") - 1
            self.save()
        return False

    @classmethod
    def send_otp(cls, user):
        otp, _ = cls.objects.update_or_create(user=user)

        send_mail(
            "Account verification",
            "Your otp is {}".format(otp.value),
            None,
            [user.email],
        )
