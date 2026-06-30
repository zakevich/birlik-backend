from django.contrib import admin

from .models import Company, CompanyUser, Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "company_type", "is_active", "created_at")
    list_filter = ("company_type", "is_active")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "internal_role", "is_active", "date_joined")
    list_filter = ("is_active", "internal_role")
    search_fields = ("username", "email", "phone")


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "role", "is_active", "created_at")
    list_filter = ("is_active", "role", "company")
    search_fields = ("user__username", "company__name", "role__name")
