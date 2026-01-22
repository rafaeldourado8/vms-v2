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

    list_display = ["email", "name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["email", "name"]
    filter_horizontal = ["roles"]
    readonly_fields = ["id", "created_at", "updated_at", "login_attempts"]

    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Status", {"fields": ("is_active", "login_attempts")}),
        ("Roles", {"fields": ("roles",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
