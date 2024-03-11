from django.urls import path

from base_app.views.admin import (
    AdminRenterRegisterRequestsListView,
    AdminVehicleListingRequestsListView,
    HandleRejectVehicleListingRequest,
    HandleAcceptVehicleListingRequest,
    HandleRejectRegisterRequest,
    HandleAcceptRegisterRequest
)


urlpatterns = [
    path(
        "pwuser/renter_requests/",
        AdminRenterRegisterRequestsListView.as_view(),
        name="admin_renter_register_list",
    ),
    path(
        "pwuser/vehicle_listing_requests/",
        AdminVehicleListingRequestsListView.as_view(),
        name="admin_vehicle_listing_request_list",
    ),
    path(
        "pwuser/vehicle_listing_requests/reject/<str:request_id>",
        HandleRejectVehicleListingRequest.as_view(),
        name="admin_vehicle_listing_request_reject"
    ),
    path(
        "pwuser/vehicle_listing_requests/accept/<str:request_id>",
        HandleAcceptVehicleListingRequest.as_view(),
        name="admin_vehicle_listing_request_accept"
    ),
    path(
        "pwuser/renter_requests/reject/",
        HandleRejectRegisterRequest.as_view(),
        name="admin_renter_register_reject",
    ),
    path(
        "pwuser/renter_requests/accept/",
        HandleAcceptRegisterRequest.as_view(),
        name="admin_renter_register_accept",
    ),
]
