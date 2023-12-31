from django.contrib import admin

from base_app.models import ApplicationUser, RenterUser


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_renter",
    ]


@admin.register(RenterUser)
class RenterUserAdmin(admin.ModelAdmin):
    list_display = ["renter_id", "application_user"]
