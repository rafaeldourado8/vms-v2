"""Django Admin configuration."""
from django.contrib import admin

from src.admin.infrastructure.persistence.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)


@admin.register(PermissionModel)
class PermissionAdmin(admin.ModelAdmin):
    """Permission admin."""

    list_display = ["code", "name", "created_at"]
    search_fields = ["code", "name"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(RoleModel)
class RoleAdmin(admin.ModelAdmin):
    """Role admin."""

    list_display = ["code", "name", "created_at"]
    search_fields = ["code", "name"]
    filter_horizontal = ["permissions"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ["email", "name", "id", "is_active", "is_staff", "is_superuser", "created_at"]
    list_filter = ["is_active", "is_staff", "is_superuser", "created_at"]
    search_fields = ["email", "name", "id"]
    filter_horizontal = ["roles"]
    readonly_fields = ["id", "created_at", "updated_at", "login_attempts"]

    fieldsets = (
        (None, {"fields": ("id", "email", "name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Roles", {"fields": ("roles",)}),
        ("Security", {"fields": ("login_attempts",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        """Save model with password hashing."""
        if "password" in form.changed_data:
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
