from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest
from django.views import View

from base_app.models import Notifications, Transactions, TransactionStatus, TransactionRequest
from base_app.mixins import AuthRequiredMixin


class NotificationListView(AuthRequiredMixin, View):
    redirect_if_not_authed = reverse_lazy("home")

    def get(self, request: HttpRequest):

        notifications_queryset = Notifications.objects.filter(
            notification_for=request.user,
        ).order_by("-data_generated_on")

        notifications = []
        for notification in notifications_queryset:
            if notification.is_transaction_request():
                redirect_link = notification.notification_redirect_link
                transaction_request_id = redirect_link.split("/")[-2]
                transaction_request = TransactionRequest.objects.get(reference_id=transaction_request_id)

                transaction_request_status = -1  # -1 for negative actions ( DECLINED, REJECTED, CANCELLED, FAILED)
                if transaction_request.status == TransactionStatus.PENDING:
                    transaction_request_status = 2  # 0 for PENDING
                elif transaction_request.status == TransactionStatus.ACCEPTED or transaction_request.status == TransactionStatus.COMPLETED:
                    transaction_request_status = 1  # 1 for positive actions

                notifications.append((transaction_request_status, notification))
            else:
                notifications.append((None, notification))

        # notification_queryset = Notifications.objects.filter(notification_for=request.user)

        # Flag all unread notifications(is_read=False) to read(is_read=True)
        for nf in notifications_queryset.filter(is_read=False):
            nf.is_read = True
            nf.save()

        return render(request, "base_app/notifications/notification_list.html", {
            "notifications": notifications,
        })

    def post(self, request: HttpRequest):
        notification_id = request.POST.get("notification_id")
        notification = Notifications.objects.get(reference_id=notification_id)
        notification.delete()

        return redirect(reverse("notification_list_view"))
