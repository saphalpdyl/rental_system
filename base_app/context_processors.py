from django.http import HttpRequest

from .models import Notifications


def new_notification_context(request: HttpRequest):
    context = {}
    if request.user.is_authenticated:
        context["has_new_notifications"] = Notifications.objects.filter(
            notification_for=request.user,
            is_read=False
        ).exists()

    return context
