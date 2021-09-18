from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentRegistration, Category, Department, Specialization

admin.site.register(StudentRegistration)
admin.site.register(Category)
admin.site.register(Department)
admin.site.register(Specialization)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    date_hierarchy = "date_joined"
    list_display = ("email", "phoneno", "gender", "date_joined")
    list_filter = (
        "is_superuser",
        "gender",
        "email_verified",
        "phoneno_verified",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("email", "email_verified"),
                    ("phoneno", "phoneno_verified"),
                    ("name", "dob",),
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_superuser", "is_staff", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": (("date_joined"),)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phoneno",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("id", "email", "phoneno", "name")
    ordering = ("-date_joined",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
