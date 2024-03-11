from django.urls import path

from base_app.views.home_view import HomeView
from base_app.views.notifications import (
    NotificationListView,
)

from .admin_urls import urlpatterns as admin_urlpatterns
from .auth_urls import urlpatterns as auth_urlpatterns
from .renter_urls import urlpatterns as renter_urlpatterns

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification_list_view"
    ),
]

urlpatterns += admin_urlpatterns
urlpatterns += auth_urlpatterns
urlpatterns += renter_urlpatterns
