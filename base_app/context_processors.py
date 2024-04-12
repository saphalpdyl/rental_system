from django.http import HttpRequest

from .models import Notifications, VehicleRent, VehicleRentStatus


def new_notification_context(request: HttpRequest):
    context = {}
    if request.user.is_authenticated:
        context["has_new_notifications"] = Notifications.objects.filter(
            notification_for=request.user,
            is_read=False
        ).exists()

    return context

def renting_status_context(request: HttpRequest):
    context = {}
    if request.user.is_authenticated:
        if VehicleRent.objects.filter(rent_request__buyer=request.user, status__in=[VehicleRentStatus.ACTIVE, VehicleRentStatus.EXPIRED]).exists():
            context['is_renting_currently'] = True
    
    return context