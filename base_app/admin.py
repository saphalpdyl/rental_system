from django.contrib import admin

from base_app.models import (
    ApplicationUser,
    RenterUser,
    RenterRegisterRequests,
    AdminUser,
    RenterRegisterResults,
    Vehicles,
    VehicleListingRequests,
    Notifications,
    VehicleRentingRequests,
    VehicleRent,
    Transactions,
    TransactionRequest,
    Review
)


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


@admin.register(RenterRegisterRequests)
class RenterRegisterRequestsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "application_user",
        "is_reviewed",
        "data_generated_on",
    ]


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ["admin_id", "application_user"]


@admin.register(RenterRegisterResults)
class RenterRegisterResultsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "data_generated_on",
        "is_approved",
        "reviewed_by",
        "renter_request",
    ]


@admin.register(Vehicles)
class VehiclesAdminView(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "vehicle_name",
        "can_be_listed",
        "is_available",
        "is_booked",
    ]


@admin.register(VehicleListingRequests)
class VehicleListingRequestsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "vehicle",
        "is_reviewed",
        "data_generated_on",
    ]


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "data_generated_on",
        "message",
        "notification_for",
        "is_read"
    ]


@admin.register(VehicleRentingRequests)
class VehicleRentingRequestsAdmin(admin.ModelAdmin):
    list_display = [
        "buyer",
        "vehicle",
        "renting_period",
        "status"
    ]


@admin.register(VehicleRent)
class VehicleRentAdmin(admin.ModelAdmin):
    list_display = ['rent_request', 'expires_at', 'status']


@admin.register(TransactionRequest)
class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = ['renting_request', 'status']

admin.site.register(Transactions)
admin.site.register(Review)