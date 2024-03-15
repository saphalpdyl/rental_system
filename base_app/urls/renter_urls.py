from django.urls import path

from base_app.views.renter import (
    VehicleAddForListingView,
    HandleCreateRenterRegisterRequest,
    RenterDashboardVehicleListView
)

urlpatterns = [
    path("myrenter/add/", VehicleAddForListingView.as_view(), name="vehicle_add"),
    path(
        "renter/register_as_renter/",
        HandleCreateRenterRegisterRequest.as_view(),
        name="create_register_as_renter",
    ),
    path("myrenter/vehicles/list/", RenterDashboardVehicleListView.as_view(), name="renter_dashboard_vehicle_list"),
]
