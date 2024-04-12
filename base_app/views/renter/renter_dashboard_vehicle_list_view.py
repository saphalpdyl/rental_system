from django.shortcuts import redirect, reverse, render
from django.http import HttpRequest
from django.views import View

from base_app.models import Vehicles, VehicleRentingRequests, RentingStatus, VehicleRent, VehicleRentStatus
from base_app.mixins import AuthRequiredMixin, RenterRequiredMixin


class RenterDashboardVehicleListView(AuthRequiredMixin, RenterRequiredMixin, View):
    def get(self, request: HttpRequest):
        vehicles_of_renter = Vehicles.objects.filter(owner__application_user=request.user)
        request_count = []
        expired_rent_exists = []

        for vehicle in vehicles_of_renter:
            count = VehicleRentingRequests.objects.filter(vehicle=vehicle, status=RentingStatus.PENDING).count()
            is_rented_and_expired = VehicleRent.objects.filter(rent_request__vehicle=vehicle, status=VehicleRentStatus.EXPIRED).exists()
            request_count.append(count)
            expired_rent_exists.append(is_rented_and_expired)
        
        # Another way of doing it
        # vehicles_with_request_count_2 = []
        # for vehicle in vehicles_of_renter:
        #     count = VehicleRentingRequests.objects.filter(vehicle=vehicle, status=RentingStatus.PENDING).count()
        #     vehicles_with_request_count_2.append((count, vehicle))
        
        # Vehicles with request count
        # where each element is a tuple in the form of ( pending_request_count, vehicle)
        # For example: ( 6, Vehicle<ZL1>)
        vehicles_with_request_count = list(zip(request_count, expired_rent_exists, vehicles_of_renter))

        return render(request, "base_app/renter/renter_dashboard_vehicle_list.html", {
            "vehicles": vehicles_of_renter,
            "vehicles_with_request_count": vehicles_with_request_count,
        })