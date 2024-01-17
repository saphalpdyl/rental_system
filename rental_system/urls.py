from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from base_app.views import (
    home_view,
    login_view,
    logout_view,
    register_view,
    admin_renter_register_requests_list_view,
    admin_vehicle_listing_requests_list_view,
    vehicle_add_for_listing_view,
    handle_create_renter_register_request,
    handle_reject_register_request,
    handle_accept_register_request,
    handle_reject_vehicle_listing_requests,
    handle_accept_vehicle_listing_requests
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path(
        "renter/register_as_renter/",
        handle_create_renter_register_request,
        name="create_register_as_renter",
    ),
    path("myrenter/add/", vehicle_add_for_listing_view, name="vehicle_add"),
    path(
        "pwuser/renter_requests/",
        admin_renter_register_requests_list_view,
        name="admin_renter_register_list",
    ),
    path(
        "pwuser/vehicle_listing_requests/",
        admin_vehicle_listing_requests_list_view,
        name="admin_vehicle_listing_request_list",
    ),
    path(
        "pwuser/vehicle_listing_requests/reject/<str:request_id>",
        handle_reject_vehicle_listing_requests,
        name="admin_vehicle_listing_request_reject"
    ),
    path(
        "pwuser/vehicle_listing_requests/accept/<str:request_id>",
        handle_accept_vehicle_listing_requests,
        name="admin_vehicle_listing_request_accept"
    ),
    path(
        "pwuser/renter_requests/reject/",
        handle_reject_register_request,
        name="admin_renter_register_reject",
    ),
    path(
        "pwuser/renter_requests/accept/",
        handle_accept_register_request,
        name="admin_renter_register_accept",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
