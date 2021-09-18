from django import db
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
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

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    image = models.ImageField(upload_to="profile")
    email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    phoneno = models.CharField("phone number", max_length=255, null=True, blank=True)
    phoneno_verified = models.BooleanField(
        default=False, verbose_name="Phone number verified"
    )
    dob = models.DateField(null=True, verbose_name="Date of birth", blank=True)
    gender = models.CharField(choices=GENDER, max_length=15, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email


class Department(models.Model):
    value = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.value


class Specialization(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.value


class Category(models.Model):
    value = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.value

    class Meta:
        verbose_name_plural = "Categories"


class StudentRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    application_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
    aadhar = models.CharField(max_length=15, unique=True, null=True, blank=True)
    passport = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    specialization = models.CharField(
        max_length=100, db_index=True, null=True, blank=True
    )
    category = models.CharField(max_length=15, db_index=True, null=True, blank=True)
    pwd = models.BooleanField(default=False)
    documents = models.TextField(
        "URL of document uploaded", help_text="comma seperated", blank=True, null=True
    )
    notes = models.TextField()

    def __str__(self):
        return self.user
