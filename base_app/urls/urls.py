from django.urls import path

from base_app.views.home_view import HomeView
from base_app.views.user_profile_view import UserProfileView
from base_app.views.handlers import (
    HandleProfilePictureChange,
    HandleProfilePictureRemove
)

from base_app.views.transactions import (
    TransactionConfirmCodeView,
    TransactionInitiateView,
    TransactionRequestRespondView
)

from base_app.views.notifications import (
    NotificationListView,
)
from base_app.views.buyer import (
    BuyerVehicleListView,
    BuyerVehicleDetailsView,
    # TransactionRequestRespondView,
    CurrentRentDetailsView,
    BuyerRentingHistoryView
)

from base_app.views.reviews import (
    VehicleReviewCreateView,
    UserProfileMyReviewsView,
)

from .admin_urls import urlpatterns as admin_urlpatterns
from .auth_urls import urlpatterns as auth_urlpatterns
from .renter_urls import urlpatterns as renter_urlpatterns

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path("user/profile/picture_change/", HandleProfilePictureChange.as_view(), name="user_profile_picture_change"),
    path("user/profile/picture_remove/", HandleProfilePictureRemove.as_view(), name="user_profile_picture_remove"),
    path("user/profile/myreviews/", UserProfileMyReviewsView.as_view(), name="user_profile_myreviews"),
    path("user/profile/myrentinghistory/", BuyerRentingHistoryView.as_view(), name="user_profile_myrentinghistory"),
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification_list_view"
    ),
    path("vehicles/", BuyerVehicleListView.as_view(), name="buyer_vehicle_list"),
    path("vehicles/<str:vehicle_id>/", BuyerVehicleDetailsView.as_view(), name="buyer_vehicle_details"),
    path("current_rents/", CurrentRentDetailsView.as_view(), name="current_rents"),
    # path("transaction/respond/<str:request_id>/", TransactionRequestRespondView.as_view(), name="transaction_request_respond"),
    path("transactions/request/respond/<str:tr_request_id>/", TransactionRequestRespondView.as_view(), name="transaction_request_respond"),
    path("payment/initiate/", TransactionInitiateView.as_view(), name="payment_initiate"),
    path("payment/initiate/code/", TransactionConfirmCodeView.as_view(), name="payment_initiate_confirm_code"),
    path("vehicles/review/create/<str:vehicle_rent_id>/", VehicleReviewCreateView.as_view(), name="vehicle_review_create")
]

urlpatterns += admin_urlpatterns
urlpatterns += auth_urlpatterns
urlpatterns += renter_urlpatterns
