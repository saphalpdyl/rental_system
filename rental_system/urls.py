from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from base_app.views import (
    HomeView,
    LoginView,
    HandleLogout,
    RegisterView,
    AdminRenterRegisterRequestsListView,
    AdminVehicleListingRequestsListView,
    VehicleAddForListingView,
    NotificationListView,
    HandleCreateRenterRegisterRequest,
    HandleRejectRegisterRequest,
    HandleAcceptRegisterRequest,
    HandleRejectVehicleListingRequest,
    HandleAcceptVehicleListingRequest
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", HandleLogout.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "renter/register_as_renter/",
        HandleCreateRenterRegisterRequest.as_view(),
        name="create_register_as_renter",
    ),
    path("myrenter/add/", VehicleAddForListingView.as_view(), name="vehicle_add"),
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
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification_list_view"
    )
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
