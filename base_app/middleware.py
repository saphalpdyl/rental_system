from django.db.models import Q
from django.utils import timezone

from base_app.models import VehicleRent, VehicleRentStatus


class ServiceExpiryCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check every user_service objects in UserService model for active until expiration
        # vehicle_rents = VehicleRent.objects.filter(Q(status=VehicleRentStatus.ACTIVE) | Q(status=VehicleRentStatus.EXTENDED))
        vehicle_rents = VehicleRent.objects.filter(status__in=[VehicleRentStatus.ACTIVE, VehicleRentStatus.EXTENDED])
        print("Hello World")
        for rent in vehicle_rents:
            if timezone.now() > rent.expires_at:
                rent.status = VehicleRentStatus.EXPIRED
                rent.save()