from django.contrib import admin

from .models import Supplier, ShopProfile, Shop, Role, User, SupplierUser, ShopUser


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "contact_person", "email", "phone")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "internal_role", "is_active", "date_joined")
    list_filter = ("is_active", "internal_role")
    search_fields = ("username", "email", "phone")

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "contact_person", "email", "phone")

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", "address", "is_active")
    list_filter = ("is_active", "profile")
    search_fields = ("name", "address", "profile__name")

@admin.register(SupplierUser)
class SupplierUserAdmin(admin.ModelAdmin):
    list_display = ("user", "supplier", "role", "is_active", "created_at")
    list_filter = ("is_active", "role", "supplier")
    search_fields = ("user__username", "supplier__name", "role__name")

@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ("user", "shop", "role", "is_active", "created_at")
    list_filter = ("is_active", "role", "shop_profile", "assigned_shop")
    search_fields = ("user__username", "shop_profile__name", "assigned_shop__name", "role__name")