from django.shortcuts import redirect, reverse, render
from django.http import HttpRequest
from django.views import View

from base_app.models import Vehicles
from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin


class RenterDashboardVehicleListView(AuthRequiredMixin, RenterRequiredMixin, View):
    def get(self, request: HttpRequest):
        vehicles_of_renter = Vehicles.objects.filter(owner__application_user=request.user)

        return render(request, "base_app/renter/renter_dashboard_vehicle_list.html", {
            "vehicles": vehicles_of_renter,
        })
