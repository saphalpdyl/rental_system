from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from base_app.models import VehicleRent, VehicleRentStatus
from base_app.mixins import AuthRequiredMixin


class CurrentRentDetailsView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        vehicle_rents = VehicleRent.objects.filter(rent_request__buyer=request.user, status__in=[VehicleRentStatus.ACTIVE, VehicleRentStatus.EXPIRED])

        return render(request, "base_app/buyer/current_rent_details.html", {
            "vehicle_rents": vehicle_rents,
        })
