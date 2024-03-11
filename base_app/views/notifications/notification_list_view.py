from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest
from django.views import View

from base_app.models import Notifications
from base_app.mixins import AuthRequiredMixin


class NotificationListView(AuthRequiredMixin, View):
    redirect_if_not_authed = reverse_lazy("home")

    def get(self, request: HttpRequest):
        notification_queryset = Notifications.objects.filter(notification_for=request.user)

        # Flag all unread notifications(is_read=False) to read(is_read=True)
        for nf in notification_queryset.filter(is_read=False):
            nf.is_read = True
            nf.save()

        return render(request, "base_app/notifications/notification_list.html", {
            "notifications": notification_queryset,
        })

    def post(self, request: HttpRequest):
        notification_id = request.POST.get("notification_id")
        notification = Notifications.objects.get(reference_id=notification_id)
        notification.delete()

        return redirect(reverse("notification_list_view"))
